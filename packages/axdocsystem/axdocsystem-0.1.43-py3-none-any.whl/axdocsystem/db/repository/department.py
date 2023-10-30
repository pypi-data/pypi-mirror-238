from sqlalchemy import select
from sqlalchemy.orm import selectinload
from axdocsystem.db.models import Department as Model
from axdocsystem.db.schemas import DepartmentSchema as Schema
from axdocsystem.db.schemas import DepartmentFullSchema as FullSchema
from .base import BaseRepository


class DepartmentRepository(BaseRepository[Model, Schema, FullSchema]):
    @property
    def _base_get_query(self):
        return (
            select(self.Model)
            .options(selectinload(self.Model.organization))
        )

    @property
    def _base_all_query(self):
        return self._base_get_query

