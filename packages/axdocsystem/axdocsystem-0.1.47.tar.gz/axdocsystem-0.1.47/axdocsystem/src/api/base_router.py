from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from axdocsystem.db.types import TUOWFactory
from axdocsystem.utils.auth_system import AuthSystem
from axdocsystem.utils.settings import JWTSettings


class BaseAuthDependentRouter(APIRouter):
    OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="api/auth/login")
    CREDENTIALS_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"msg": "Could not validate credentials"},
        headers={"WWW-Authenticate": "Bearer"},
    )

    def __init__(self, *args, uowf: TUOWFactory, settings: JWTSettings, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.uowf = uowf
        self.exclude_auth_endpoints = ["/login", "/verify", "/forgot", "/refresh"]
        self.exclude_non_auth_endpoints = ["/admin", "/admins"]
        self.auth_system = AuthSystem(settings)

    async def auth_dependency(self, request: Request, token: str = Depends(OAUTH2_SCHEME)):
        try:
            email = self.auth_system.get_token_data(token)
        except Exception:
            raise self.CREDENTIALS_EXCEPTION
        
        async with self.uowf() as uow:
            admin = await uow.repo.users.get(email) 
            
        if admin is None:
            raise self.CREDENTIALS_EXCEPTION
       
        request.state.admin = admin

    def default_route(self, method):
        def wrapper(*args, **kwargs):
            return self.api_route(*args, methods=[method], **kwargs)

        return wrapper

    def __getattribute__(self, name: str):
        methods_list = ["get", "post", "put", "patch", "delete"]
        if name.lower() in methods_list:
            return self.default_route(name.upper())
        return super().__getattribute__(name)

    def api_route(self, path, *args, methods, dependencies=None, use_default_deps=True, **kwargs):
        is_force_non_auth = path in self.exclude_auth_endpoints or "GET" in methods
        is_force_auth = path in self.exclude_non_auth_endpoints
        if use_default_deps and (is_force_auth or not is_force_non_auth):
            if dependencies is None:
                dependencies = ()
            dependencies = [Depends(self.auth_dependency), *dependencies]
        return super().api_route(path, *args, methods=methods, dependencies=dependencies, **kwargs)


