from typing import Type
from axsqlalchemy.repository import BaseRepository
from fastapi import Depends, File, UploadFile

from pydantic import BaseModel
from axdocsystem.db.schemas import DocumentSchema
from axdocsystem.src.api.base import Request, with_uow
from axdocsystem.src.api.schemas import DocumentsPostSchema
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
    async def create(self, req: Request, data: DocumentsPostSchema = Depends(), file: UploadFile = File(...)):
        item = DocumentSchema(**data.dict())
        item.file_name, item.file_size  = await self.document_saver.save_document(item.file_name, file)
        await req.state.uow.repo.document.add(item)


