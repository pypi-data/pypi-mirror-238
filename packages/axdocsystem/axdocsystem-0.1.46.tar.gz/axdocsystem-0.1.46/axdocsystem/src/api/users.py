from typing import Optional, Type
from axsqlalchemy.repository import BaseRepository

from pydantic import BaseModel
from axdocsystem.db.models import Department, Users
from axdocsystem.db.schemas import QuickSearchResult, UsersSchema
from axdocsystem.src.api.base import Request, with_uow
from axdocsystem.src.api.schemas import UsersPostSchema
from .base_crud_api import BaseCRUDApi


class UsersApi(BaseCRUDApi):
    @property
    def schema(self) -> Type[BaseModel]:
        return UsersSchema

    @property
    def schema_create(self):
        return UsersPostSchema 

    def get_repo(self, req: Request) -> BaseRepository:
        return req.state.uow.repo.users

    def get_quick_search_pattern_filters(self, req: Request, pattern: str):
        return (getattr(self.find_repo(req).Model, 'fullname').ilike(f'%{pattern}%'),)

    def get_item_as_quick_search_result(self, item: UsersSchema):
        return QuickSearchResult(
            id=item.email,
            name=item.fullname,
        )

    async def all(
        self, 
        req: Request, 
        email: Optional[str] = None, 
        deparment_name: Optional[str] = None, 
        fullname: Optional[str] = None, 
        page: int = 1, 
        count: int = 10,
    ):
        req.state.filters = []

        if email:
            req.state.filters.append(Users.email.ilike(f'%{email}%'))
        if fullname:
            req.state.filters.append(Users.fullname.ilike(f'%{fullname}%'))
        if deparment_name:
            req.state.filters.append(Department.name.ilike(f'%{deparment_name}%'))

        return await super().all(req=req, page=page, count=count)

