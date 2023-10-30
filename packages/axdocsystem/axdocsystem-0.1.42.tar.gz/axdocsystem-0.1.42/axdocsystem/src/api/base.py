from abc import ABC, abstractmethod
from typing import Iterable, Optional, Union
from fastapi import APIRouter, Request as _Request
from functools import wraps

from axdocsystem.db.schemas import UsersSchema
from axdocsystem.utils.settings import JWTSettings
from .base_router import BaseAuthDependentRouter 
from axdocsystem.db.types import TUOWFactory, TUOW


class State:
    uow: TUOW
    admin: UsersSchema
    filters: Optional[Iterable] = None


class Request(_Request):
    state: State


class BaseApi(ABC):
    def __init__(self, uowf: TUOWFactory, settings: JWTSettings,  router: Union[BaseAuthDependentRouter, None] = None) -> None:
        self.router = router or BaseAuthDependentRouter(uowf=uowf, settings=settings)
        self.register_router(self.router)
        self.uowf = uowf

    @abstractmethod
    def register_router(self, router: BaseAuthDependentRouter) -> APIRouter:
        raise NotImplementedError


def with_uow(f):
    @wraps(f)
    async def wrapper(self: BaseApi, *args, req: Request, **kwargs):
        async with self.uowf() as uow:
            req.state.uow = uow
            return await f(self, *args, req=req, **kwargs)
    
    return wrapper

