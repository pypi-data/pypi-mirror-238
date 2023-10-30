from axdocsystem.db.models import Users as Model
from axdocsystem.db.schemas import UsersSchema as Schema
from .base import BaseRepository


class UsersRepository(BaseRepository[Model, Schema, Schema]):
    pass

