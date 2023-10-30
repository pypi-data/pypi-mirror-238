from typing import Type
from axsqlalchemy.repository import BaseRepository

from pydantic import BaseModel
from axdocsystem.db.schemas import DepartmentSchema
from axdocsystem.src.api.base import Request
from .base_crud_api import BaseCRUDApi


class DepartmentApi(BaseCRUDApi):
    @property
    def schema(self) -> Type[BaseModel]:
        return DepartmentSchema

    def get_repo(self, req: Request) -> BaseRepository:
        return req.state.uow.repo.department

