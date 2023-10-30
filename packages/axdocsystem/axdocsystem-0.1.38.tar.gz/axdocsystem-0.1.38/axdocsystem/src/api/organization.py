from typing import Optional, Type
from axsqlalchemy.repository import BaseRepository

from pydantic import BaseModel
from axdocsystem.db.schemas import OrganizationSchema
from axdocsystem.db.models import Organization as OrganizationModel
from axdocsystem.src.api.base import Request
from .base_crud_api import BaseCRUDApi


class OrganizationApi(BaseCRUDApi):
    @property
    def schema(self) -> Type[BaseModel]:
        return OrganizationSchema

    def get_repo(self, req: Request) -> BaseRepository:
        return req.state.uow.repo.organization

    async def all(self, req: Request, name: Optional[str] = None, page: int = 1, count: int = 10):
        if name:
            req.state.filters = (
                OrganizationModel.name.ilike(f'%{name}%'),
            )
        return await super().all(req=req, page=page, count=count)

