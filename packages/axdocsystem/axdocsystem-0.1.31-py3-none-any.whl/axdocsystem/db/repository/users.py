from axsqlalchemy.repository import BaseRepository
from axdocsystem.db.models import Users as Model
from axdocsystem.db.schemas import UsersSchema as Schema


class UsersRepository(BaseRepository[Model, Schema, Schema]):
    pass

