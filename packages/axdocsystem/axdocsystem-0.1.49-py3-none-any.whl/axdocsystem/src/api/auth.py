from typing import Optional, Union

from aiosmtplib import SMTPRecipientRefused, SMTPRecipientsRefused
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm 
from passlib.exc import UnknownHashError
from contextlib import contextmanager
from axdocsystem.src.api.base_router import BaseAuthDependentRouter

from axdocsystem.db.schemas import UsersSchema
from axdocsystem.src.settings import Settings
from axdocsystem.utils.message_system import MessageSystem
from axdocsystem.utils.email_system import EmailSystem
from axdocsystem.utils.admin_one_time_token_manager import AdminOneTimeTokenManager

from .base import BaseApi, Request, with_uow
from .schemas import (
    UserInfoSchema,
    LoginPayloadSchema, 
    PromotionVerificationSchema, 
    ForgotSchema,
)


class AuthApi(BaseApi):
    BASE_EXCEPTION = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Почта или пароль не верный", 
    )
    NOT_ALLOWED_EXCEPTION = HTTPException(
        status_code=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
        detail="Почта или пароль не верный", 
    )
    AUTH_EXISTS_EXCEPTION = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Данная почта уже зарегистрировано", 
    )
    TOKEN_EXCEPTION = HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="Token is not valid",
    )
    EMAIL_RECIPIENT_EXCEPTION = HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Can't send verification code to recipient",
    )
 
    def __init__(self, uowf, settings: Settings, router: Union[BaseAuthDependentRouter, None] = None) -> None:
        super().__init__(uowf, settings, router)
        self.email_system = EmailSystem(settings)
        self.message_system = MessageSystem(self.email_system)
        self.settings = settings
        self.token_manager = AdminOneTimeTokenManager()

    def _validate_auth(self, plain_passwd, auth: Optional[UsersSchema] = None) -> UsersSchema:
        try:
            if not (auth and auth.password_hash and self.router.auth_system.varify_password(plain_passwd, auth.password_hash)):
                raise self.BASE_EXCEPTION
        except UnknownHashError:
            raise self.BASE_EXCEPTION
        
        return auth

    @contextmanager
    def _validate_email(self):
        try:
            yield
        except (SMTPRecipientRefused, SMTPRecipientsRefused) as e: 
            print(str(e))
            raise self.EMAIL_RECIPIENT_EXCEPTION

    @with_uow
    async def login(self, req: Request, form: OAuth2PasswordRequestForm = Depends()):
        admin = await req.state.uow.repo.users.get(form.username)
        admin = self._validate_auth(form.password, admin)
        return LoginPayloadSchema(
            user=UserInfoSchema.from_orm(admin),
            access_token=self.router.auth_system.create_access_token(admin.email),
            refresh_token=self.router.auth_system.create_refresh_token(admin.email),
        )

    @with_uow
    async def refresh(self, req: Request):
        token = req.headers.get('authorization') 
        
        try:
            email = self.router.auth_system.get_token_data(token)
        except Exception:
            raise self.TOKEN_EXCEPTION
        
        admin = await req.state.uow.repo.users.get(email)
       
        if not admin:
            raise self.TOKEN_EXCEPTION

        return LoginPayloadSchema(
            user=UserInfoSchema.from_orm(admin),
            access_token=self.router.auth_system.create_access_token(admin.email),
            refresh_token=self.router.auth_system.create_refresh_token(admin.email),
        )

    @with_uow
    async def forgot_passwd(self, req: Request, data: ForgotSchema):
        admin = await req.state.uow.repo.users.get(data.email)
        if not admin:
            raise HTTPException(404)
        
        code = self.token_manager.create(f"{admin.promoted_by}:{admin.email}")
        with self._validate_email():
            await self.message_system.send_forgot_reset_passwd_code(
                receiver=admin.email, 
                name=admin.fullname,
                code=code,
            )

    @with_uow
    async def verify_promotion(self, req: Request, data: PromotionVerificationSchema):
        sdata = self.token_manager.release(data.token)
        
        if not sdata:
            raise self.TOKEN_EXCEPTION
        
        admin_email, user_email = str(sdata).split(":")
        admin = await req.state.uow.repo.users.get(admin_email)
        user = await req.state.uow.repo.users.get(user_email)

        if not (admin and user):
            raise self.TOKEN_EXCEPTION

        pass_hash = self.router.auth_system.get_password_hash(data.password)
        await req.state.uow.repo.users.update(
            req.state.uow.repo.users.Schema(
                fullname=user.fullname,
                position=user.position,
                department_id=user.department_id,
                email=user_email,
                password_hash=pass_hash,
                phone=user.phone,
                promoted_by=admin_email,
            )
        )

    def register_router(self, router: BaseAuthDependentRouter) -> BaseAuthDependentRouter:
        router.post('/forgot', status_code=202)(self.forgot_passwd)
        router.post('/verify', status_code=202)(self.verify_promotion)
        router.post('/login', response_model=LoginPayloadSchema)(self.login)
        router.post('/refresh', response_model=LoginPayloadSchema)(self.refresh)
        return router

