from axdocsystem.db.models import Document as Model
from axdocsystem.db.schemas import DocumentSchema as Schema
from .base import BaseRepository


class DocumentRepository(BaseRepository[Model, Schema, Schema]):
    pass

