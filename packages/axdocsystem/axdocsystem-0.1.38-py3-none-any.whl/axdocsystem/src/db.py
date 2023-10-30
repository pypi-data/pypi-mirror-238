from axabc.db import AsyncUOWFactory
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from axdocsystem.db.collection import RepoCollection
from axsqlalchemy.settings import Settings as _DBSettings
from axsqlalchemy.utils.creation import create_models
from axdocsystem.db.models import Base as _DBBase


def get_uowf(settings: _DBSettings) -> AsyncUOWFactory[RepoCollection]:
    engine = create_async_engine(settings.db_connection_string)
    session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)  # type: ignore
    session_maker.engine = engine  # type: ignore
    return AsyncUOWFactory(RepoCollection, session_maker)   # type: ignore


async def setup_db(uowf: AsyncUOWFactory[RepoCollection]):
    await create_models(getattr(uowf.session_maker, 'engine'), _DBBase)

