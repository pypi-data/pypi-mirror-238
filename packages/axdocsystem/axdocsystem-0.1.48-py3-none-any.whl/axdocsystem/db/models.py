from datetime import datetime
import sqlalchemy as sa
from axsqlalchemy.model import BaseTableInt as _BaseTableInt, BaseTable as _BaseTable, Base
from sqlalchemy.orm import relationship
from .enums import DocumentStatusEnum, UsersPositionEnum


__all__ = [
    'Base',
    'Organization',
]


class BaseTable(_BaseTable):
    __abstract__ = True

    created_at = sa.Column(sa.DateTime(timezone=True), default=datetime.now)
    updated_at = sa.Column(sa.DateTime(timezone=True), onupdate=datetime.now)


class BaseTableInt(_BaseTableInt, BaseTable):
    __abstract__ = True


class Organization(BaseTableInt):
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)
    description = sa.Column(sa.String)


class Department(BaseTableInt):
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)
    organization_id = sa.Column(sa.ForeignKey(Organization.id))
    organization = relationship('Organization', innerjoin=True)

    @property
    def organization_name(self) -> str:
        return (self.organization and self.organization.name) or ""


class Users(BaseTable):
    email = sa.Column(sa.String(255), primary_key=True)
    fullname = sa.Column(sa.String(255), nullable=False)
    department_id = sa.Column(sa.ForeignKey(Department.id))
    position = sa.Column(sa.Enum(UsersPositionEnum))
    phone = sa.Column(sa.String(255), nullable=False)
    password_hash = sa.Column(sa.String(255), nullable=True)
    promoted_by = sa.Column(sa.ForeignKey('users.email'), nullable=True)
    is_verified = sa.Column(sa.Boolean, default=False) 
    department = relationship('Department', innerjoin=True)

    @property
    def department_name(self) -> str:
        return (self.department and self.department.name) or ""


class Document(BaseTableInt):
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(255))
    description = sa.Column(sa.String)
    status = sa.Column(sa.Enum(DocumentStatusEnum))

    sender_id = sa.Column(sa.ForeignKey(Users.email))
    executor_id = sa.Column(sa.ForeignKey(Users.email))

    from_org_id = sa.Column(sa.ForeignKey(Organization.id))
    to_org_id = sa.Column(sa.ForeignKey(Organization.id))

    send_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())
    received_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())
    expiring_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())

    file_name = sa.Column(sa.String(255))
    file_size = sa.Column(sa.BIGINT(), nullable=False)
    content_type = sa.Column(sa.String(255), nullable=True)

    from_org = relationship('Organization', foreign_keys=[from_org_id])
    to_org = relationship('Organization', foreign_keys=[to_org_id])

    sender_user = relationship('Users', foreign_keys=[sender_id])
    executer_user = relationship('Users', foreign_keys=[executor_id])

    # from_id = sa.Column(sa.Integer)
    # to_id = sa.Column(sa.Integer)

