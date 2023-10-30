from axsqlalchemy.repository import BaseRepository
from axdocsystem.db.models import Document as Model
from axdocsystem.db.schemas import DocumentSchema as Schema


class DocumentRepository(BaseRepository[Model, Schema, Schema]):
    pass

