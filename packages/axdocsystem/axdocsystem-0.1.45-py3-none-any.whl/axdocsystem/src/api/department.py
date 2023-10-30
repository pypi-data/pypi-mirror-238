from typing import Optional, Type
from axsqlalchemy.repository import BaseRepository

from pydantic import BaseModel
from axdocsystem.db.models import Department, Organization
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

    async def all(
        self, 
        req: Request, 
        name: Optional[str] = None, 
        organization_name: Optional[str] = None, 
        page: int = 1, 
        count: int = 10,
    ):
        req.state.filters = []

        if name:
            req.state.filters.append(Department.name.ilike(f'%{name}%'))
        if organization_name:
            req.state.filters.append(Organization.name.ilike(f'%{organization_name}%'))

        return await super().all(req=req, page=page, count=count)

