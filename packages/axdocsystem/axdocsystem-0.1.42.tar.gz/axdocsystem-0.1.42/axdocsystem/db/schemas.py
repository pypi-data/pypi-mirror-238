from datetime import datetime
from typing import Generic, Optional, TypeVar
from axsqlalchemy.schema import BaseModel
from pydantic import validator
from pydantic.generics import GenericModel

from .enums import UsersPositionEnum, DocumentStatusEnum


TPageItem = TypeVar('TPageItem', bound=BaseModel)


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
    password_hash: str
    promoted_by: Optional[str] = None


class DocumentSchema(BaseModel):
    id: Optional[int] = None
    title: str
    sender_id: str
    executor_id: str
    file_name: str
    description: Optional[str]
    from_id: int
    to_id: int
    status: DocumentStatusEnum
    from_org_id: int
    to_org_id: int
    send_at: datetime
    received_at: datetime
    expiring_at: datetime

