from datetime import datetime
from typing import Generic, Optional, TypeVar
from uuid import uuid4
from axsqlalchemy.schema import BaseModel, Field
from pydantic import validator, BaseModel as _BaseModel
from pydantic.generics import GenericModel

from .enums import UsersPositionEnum, DocumentStatusEnum


TPageItem = TypeVar('TPageItem', bound=_BaseModel)


class QuickSearchResult(_BaseModel):
    id: str | int
    name: str


class Page(GenericModel, Generic[TPageItem]):
    all_page_count: int
    items: list[TPageItem]


class OrganizationSchema(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str]

    @validator("name")
    def price_must_not_be_negative(cls, value: str):
        if len(value) < 5:
            raise ValueError("Длинна названия должно быть больше 5")
        return value


class DepartmentSchema(BaseModel):
    id: Optional[int] = None
    name: str
    organization_id: int


class DepartmentFullSchema(DepartmentSchema):
    organization: Optional[OrganizationSchema] = None
    organization_name: str


class UsersSchema(BaseModel):
    email: str
    fullname: str
    department_id: Optional[int] = None
    position: Optional[UsersPositionEnum] = None
    phone: str
    password: Optional[str] = None
    password_hash: Optional[str] = None
    promoted_by: Optional[str] = None
    is_verified: bool = False


class UsersFullSchema(UsersSchema):
    department_name: str


class DocumentSchema(BaseModel):
    id: Optional[int] = None
    title: str
    sender_id: str
    executor_id: str
    file_name: str = Field(default_factory=lambda: str(uuid4()))
    file_size: int = 0
    description: Optional[str]
    status: DocumentStatusEnum
    from_org_id: int
    to_org_id: int
    send_at: datetime
    received_at: datetime
    expiring_at: datetime


class DocumentFullSchema(DocumentSchema):
    from_org: Optional[OrganizationSchema] = None
    to_org: Optional[OrganizationSchema] = None

    sender_user: Optional[UsersSchema] = None
    executer_user: Optional[UsersSchema] = None
