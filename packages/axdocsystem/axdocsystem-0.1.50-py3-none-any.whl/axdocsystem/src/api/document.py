from typing import Type
from axsqlalchemy.repository import BaseRepository
from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile, status
from fastapi.responses import FileResponse

from pydantic import BaseModel
from pydantic.main import Optional
from sqlalchemy import or_
from axdocsystem.db.models import Document, Users
from axdocsystem.db.repository.document import ExecuterUser, FromOrganization, SenderUser, ToOrganization
from axdocsystem.db.schemas import DocumentSchema, QuickSearchResult
from axdocsystem.src.api.base import Request, with_uow
from axdocsystem.src.api.schemas import DocumentsFullPutSchema, DocumentsPostSchema, DocumentsPutSchema
from axdocsystem.utils.document_saver import DocumentSaver
from axdocsystem.db.schemas import DocumentFullSchema as FullSchema
from .base_crud_api import BaseCRUDApi


class DocumentApi(BaseCRUDApi):
    def __init__(self, uowf, settings, router = None) -> None:
        super().__init__(uowf, settings, router)
        self.document_saver = DocumentSaver()

    @property
    def schema(self) -> Type[BaseModel]:
        return DocumentSchema

    @property
    def schema_create(self):
        return DocumentsPostSchema

    @property
    def schema_full(self):
        return FullSchema

    def get_repo(self, req: Request) -> BaseRepository:
        return req.state.uow.repo.document

    @with_uow
    async def create(self, req: Request, data: DocumentsPostSchema = Depends(), file: Optional[UploadFile] = File(None)):
        if not file:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=[{'msg': 'Файл является объязательным'}],
            )

        item = DocumentSchema(**data.dict())
        item.file_name, item.file_size  = await self.document_saver.save_document(item.file_name, file)
        item.file_external_name = file.filename
        item.content_type = file.content_type

        await req.state.uow.repo.document.add(item)

    @with_uow
    async def update(self, req: Request, data: DocumentsPutSchema = Depends(), file: Optional[UploadFile] = File(None)):
        if not (data.id and (previous := await req.state.uow.repo.document.get(data.id))):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=[{'msg': 'Документ не найден'}],
            )

        item = data

        if file:
            item = DocumentsFullPutSchema(**data.dict())
            item.file_name, item.file_size  = await self.document_saver.save_document(item.file_name, file)
            item.content_type = file.content_type
            item.file_external_name = file.filename

        await req.state.uow.repo.document.update(item)  # type: ignore

    @with_uow
    async def get_blob(self, req: Request, id: int):
        if not (document := await req.state.uow.repo.document.get(id)):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=[{'msg': 'Файл не найден'}],
            )

        return Response(
            await (self.document_saver.get_bytes(document.file_name)), 
            media_type=document.content_type,
            headers={
                'Content-Disposition': (
                    'attachment; '
                    f'filename="{document.file_external_name or document.file_name}"'
                )
            }
        )

    async def all(
        self, 
        req: Request, 
        title: Optional[str] = None, 
        user: Optional[str] = None,
        organization: Optional[str] = None,
        page: int = 1, 
        count: int = 10,
    ):
        req.state.filters = []

        if title:
            req.state.filters.append(Document.title.ilike(f'%{title}%'))
        if user:
            req.state.filters.append(
                or_(
                    ExecuterUser.fullname.ilike(f'%{user}%'),
                    ExecuterUser.email.ilike(f'%{user}%'),
                    SenderUser.fullname.ilike(f'%{user}%'),
                    SenderUser.email.ilike(f'%{user}%'),
                )
            )
        if organization:
            req.state.filters.append(
                or_(
                    FromOrganization.name.ilike(f'%{organization}%'),
                    FromOrganization.description.ilike(f'%{organization}%'),
                    ToOrganization.name.ilike(f'%{organization}%'),
                    ToOrganization.description.ilike(f'%{organization}%'),
                )
            )

        return await super().all(req=req, page=page, count=count)

    def get_quick_search_pattern_filters(self, _: Request, pattern: str):
        return (Document.title.ilike(f'%{pattern}%'),)

    def get_item_as_quick_search_result(self, item: DocumentSchema):
        return QuickSearchResult(
            id=str(item.id),
            name=item.title,
        )

    def register_router(self, router) -> APIRouter:
        router = super().register_router(router)
        router.get('/blob/{id}', response_class=FileResponse)(self.get_blob)
        return router

