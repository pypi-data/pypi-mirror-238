from typing import Generic
from axsqlalchemy.repository import BaseRepository as _BaseRepository
from axsqlalchemy.repository.types import TDBModel, TIModel, TOModel


class BaseRepository(
	_BaseRepository[TDBModel, TIModel, TOModel],
    Generic[TDBModel, TIModel, TOModel],
):
    __abstract__ = True

    async def add(self, obj: TIModel, autosave=True) -> TIModel:
        if type(obj) in (self.OSchema, self.Schema):
            obj = self.Schema.from_orm(obj)

        mobj = self.Model(**obj.dict())
        self.session.add(mobj)
        
        if autosave:
            await self.session.commit()

        return self.Schema.from_orm(mobj)

