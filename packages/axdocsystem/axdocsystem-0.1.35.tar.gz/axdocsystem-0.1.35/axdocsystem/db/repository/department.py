from axsqlalchemy.repository import BaseRepository
from axdocsystem.db.models import Department as Model
from axdocsystem.db.schemas import DepartmentSchema as Schema


class DepartmentRepository(BaseRepository[Model, Schema, Schema]):
    pass

