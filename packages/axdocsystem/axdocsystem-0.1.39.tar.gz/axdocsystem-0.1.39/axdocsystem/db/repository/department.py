from sqlalchemy import select
from axdocsystem.db.models import Department as Model
from axdocsystem.db.models import Organization as OrganizationModel
from axdocsystem.db.schemas import DepartmentSchema as Schema
from axdocsystem.db.schemas import DepartmentFullSchema as FullSchema
from .base import BaseRepository


class DepartmentRepository(BaseRepository[Model, Schema, FullSchema]):
    @property
    def _base_all_query(self):
        return (
            select(self.Model)
            .join(OrganizationModel, onclause=OrganizationModel.id==self.Model.organization_id)
        )

