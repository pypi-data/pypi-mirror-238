from typing import Type
from axsqlalchemy.repository import BaseRepository

from pydantic import BaseModel
from axdocsystem.db.schemas import DepartmentSchema, DepartmentFullSchema
from axdocsystem.src.api.base import Request
from .base_crud_api import BaseCRUDApi


class DepartmentApi(BaseCRUDApi):
    @property
    def schema(self) -> Type[BaseModel]:
        return DepartmentSchema

    @property
    def schema_full(self):
        return DepartmentFullSchema 

    def get_repo(self, req: Request) -> BaseRepository:
        return req.state.uow.repo.department

