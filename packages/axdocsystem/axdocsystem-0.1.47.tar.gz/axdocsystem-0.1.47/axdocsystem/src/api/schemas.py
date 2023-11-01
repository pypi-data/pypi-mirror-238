from datetime import datetime
from typing import Optional
from uuid import uuid4
from pydantic import BaseModel as _BaseModel
from pydantic.main import Field
from axdocsystem.db.enums import DocumentStatusEnum, UsersPositionEnum
from axdocsystem.db.schemas import BaseModel


class DocumentsPostSchema(_BaseModel):
    title: str
    sender_id: str
    executor_id: str
    description: Optional[str]
    status: DocumentStatusEnum
    from_org_id: int
    to_org_id: int
    send_at: datetime
    received_at: datetime
    expiring_at: datetime


class DocumentsPutSchema(DocumentsPostSchema):
    id: Optional[int] = None


class DocumentsFullPutSchema(DocumentsPostSchema):
    id: Optional[int] = None
    file_name: str = Field(default_factory=lambda: str(uuid4()))
    file_size: int = 0
    content_type: Optional[str] = None


class UsersPostSchema(_BaseModel):
    email: str
    fullname: str
    department_id: Optional[int] = None
    position: Optional[UsersPositionEnum] = None
    phone: str
    promoted_by: Optional[str] = None


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

