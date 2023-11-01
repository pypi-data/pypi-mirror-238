from axdocsystem.db.models import Organization as Model
from axdocsystem.db.schemas import OrganizationSchema as Schema
from .base import BaseRepository


class OrganizationRepository(BaseRepository[Model, Schema, Schema]):
    pass

