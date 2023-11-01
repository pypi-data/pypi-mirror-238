from typing import Type
from axsqlalchemy.repository import BaseRepository
from fastapi import Depends, File, HTTPException, UploadFile, status

from pydantic import BaseModel
from pydantic.main import Optional
from axdocsystem.db.schemas import DocumentSchema
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
            item.id = previous.id
            item = DocumentsFullPutSchema(**data.dict())
            item.created_at = previous.created_at
            item.file_name, item.file_size  = await self.document_saver.save_document(item.file_name, file)
            item.content_type = file.content_type

        await req.state.uow.repo.document.update(item)  # type: ignore

