from typing import Type
from axsqlalchemy.repository import BaseRepository

from pydantic import BaseModel
from axdocsystem.db.schemas import UsersSchema
from axdocsystem.src.api.base import Request
from .base_crud_api import BaseCRUDApi


class UsersApi(BaseCRUDApi):
    @property
    def schema(self) -> Type[BaseModel]:
        return UsersSchema

    def get_repo(self, req: Request) -> BaseRepository:
        return req.state.uow.repo.users

