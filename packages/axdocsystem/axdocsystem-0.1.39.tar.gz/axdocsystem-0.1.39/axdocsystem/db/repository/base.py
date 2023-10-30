from typing import Generic
from axsqlalchemy.repository import BaseRepository as _BaseRepository
from axsqlalchemy.repository.types import TDBModel, TIModel, TOModel


class BaseRepository(
	_BaseRepository[TDBModel, TIModel, TOModel],
    Generic[TDBModel, TIModel, TOModel],
):
    __abstract__ = True


