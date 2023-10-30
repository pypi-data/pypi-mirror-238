from abc import abstractmethod
from typing import Type
from axsqlalchemy.repository.paginated import math
from fastapi import APIRouter
from pydantic import parse_obj_as
from sqlalchemy.sql.selectable import Optional
from axdocsystem.db.schemas import Page, QuickSearchResult
from axdocsystem.src.api.base_router import BaseAuthDependentRouter
from axsqlalchemy.repository import BaseRepository
from axsqlalchemy.schema import BaseModel as BaseSchemaModel
from .base import BaseApi, with_uow, Request


class BaseCRUDApi(BaseApi):
    DEFAULT_FILTERS = tuple()

    @property
    @abstractmethod
    def schema(self) -> Type[BaseSchemaModel]:
        raise NotImplementedError

    @property
    def schema_full(self) -> Optional[Type[BaseSchemaModel]]:
        return None

    @abstractmethod
    def get_repo(self, req: Request) -> BaseRepository:
        raise NotImplementedError

    def find_repo(self, req: Request) -> BaseRepository:
        return self.get_repo(req)

    def _create(self):
        async def create(req: Request, data: self.schema):  # type: ignore
            async with self.uowf() as uow:
                req.state.uow = uow
                await self.find_repo(req).add(data)

        return create

    def _update(self):
        async def update(req: Request, data: self.schema):  # type: ignore
            async with self.uowf() as uow:
                req.state.uow = uow
                await self.find_repo(req).update(data)

        return update

    @with_uow
    async def delete(self, req: Request, id: int):
        await self.find_repo(req).delete(id)

    @with_uow
    async def get(self, req: Request, id: int):
        return await self.find_repo(req).get(id)

    @with_uow
    async def all(self, req: Request, page: int = 1, count: int = 10):
        all_count = await self.find_repo(req).all_count()
        all_page_count = math.ceil(all_count / count) if count else 1
        filters = getattr(req.state, 'filters', self.DEFAULT_FILTERS)
        items = await self.find_repo(req).all(page=int(page), count=int(count), filters=filters)

        return parse_obj_as(Page[self.schema], {
            'all_page_count': all_page_count,
            'items': items,
        })

    def get_quick_search_pattern_filters(self, req: Request, pattern: str):
        return (getattr(self.find_repo(req).Model, 'name').ilike(f'%{pattern}%'),)

    def get_item_as_quick_search_result(self, item):
        print(f"{getattr(item, 'id')=}")
        return QuickSearchResult(
            id=int(getattr(item, 'id')),
            name=getattr(item, 'name'),
        )

    @with_uow
    async def quick_search(self, req: Request, pattern: str, page: int = 1, count: int = 10):
        all_count = await self.find_repo(req).all_count()
        all_page_count = math.ceil(all_count / count) if count else 1
        filters = self.get_quick_search_pattern_filters(req, pattern) or self.DEFAULT_FILTERS
        items = await self.find_repo(req).all(page=int(page), count=int(count), filters=filters)

        return parse_obj_as(Page[QuickSearchResult], {
            'all_page_count': all_page_count,
            'items': list(map(self.get_item_as_quick_search_result, items)),
        })
        
    def register_router(self, router: BaseAuthDependentRouter) -> APIRouter:
        router.post('/')(self._create())
        router.put('/')(self._update())
        router.delete('/{id}')(self.delete)
        router.get('/search', response_model=Page[QuickSearchResult])(self.quick_search)
        router.get('/{id}', response_model=self.schema)(self.get)
        router.get('/', response_model=Page[self.schema_full or self.schema])(self.all)

        return router

