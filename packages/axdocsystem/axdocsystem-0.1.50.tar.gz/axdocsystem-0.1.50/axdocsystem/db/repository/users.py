from sqlalchemy import select
from sqlalchemy.orm import selectinload
from axdocsystem.db.models import Department, Users as Model
from axdocsystem.db.schemas import UsersSchema as Schema
from axdocsystem.db.schemas import UsersFullSchema as FullSchema
from .base import BaseRepository


class UsersRepository(BaseRepository[Model, Schema, FullSchema]):
    @property
    def _base_get_query(self):
        return (
            select(self.Model)
            .join(
                Department,
                onclause=self.Model.department_id == Department.id,
                isouter=True,
            )
            .options(selectinload(Model.department))
        )

    @property
    def _base_all_query(self):
        return self._base_get_query

