from .collection import RepoCollection
from axabc.db import AsyncUOWFactory, AsyncUOW


TUOW = AsyncUOW[RepoCollection]
TUOWFactory = AsyncUOWFactory[RepoCollection]


__all__ = [
    'TUOW',
    'TUOWFactory',
]

