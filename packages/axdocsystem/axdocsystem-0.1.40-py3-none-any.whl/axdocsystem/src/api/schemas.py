from axdocsystem.db.schemas import BaseModel


class UserInfoSchema(BaseModel):
    fullname: str


class LoginSchemas(BaseModel):
    username: str
    password: str


class LoginPayloadSchema(BaseModel):
    user: UserInfoSchema
    access_token: str
    refresh_token: str


class ForgotSchema(BaseModel):
    email: str


class PromotionCreationSchema(ForgotSchema):
    name: str


class PassUpdateSchema(BaseModel):
    old_password: str
    new_password: str


class PromotionVerificationSchema(BaseModel):
    token: str
    password: str

