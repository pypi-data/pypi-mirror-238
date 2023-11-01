from sqlalchemy.orm import aliased, selectinload
from sqlalchemy.sql import select
from axdocsystem.db.models import Document as Model, Organization, Users
from axdocsystem.db.schemas import DocumentSchema as Schema
from axdocsystem.db.schemas import DocumentFullSchema as FullSchema
from .base import BaseRepository


FromOrganization = aliased(Organization)
ToOrganization = aliased(Organization)

SenderUser = aliased(Users)
ExecuterUser = aliased(Users)


class DocumentRepository(BaseRepository[Model, Schema, FullSchema]):
    @property
    def _base_get_query(self):
        return (
            select(self.Model)
            .join(
                FromOrganization,
                onclause=self.Model.from_org_id == FromOrganization.id,
                isouter=True,
            )
            .options(selectinload(Model.from_org))
            .join(
                ToOrganization,
                onclause=self.Model.to_org_id == ToOrganization.id,
                isouter=True,
            )
            .options(selectinload(Model.to_org))
            .join(
                SenderUser,
                onclause=self.Model.sender_id == SenderUser.email,
                isouter=True,
            )
            .options(selectinload(Model.sender_user))
            .join(
                ExecuterUser,
                onclause=self.Model.executor_id == ExecuterUser.email,
                isouter=True,
            )
            .options(selectinload(Model.executer_user))
        )

    @property
    def _base_all_query(self):
        return self._base_get_query

