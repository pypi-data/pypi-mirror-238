import sqlalchemy as sa
from axsqlalchemy.model import BaseTableInt, BaseTable, Base
from sqlalchemy.orm import relationship
from .enums import DocumentStatusEnum, UsersPositionEnum


__all__ = [
    'Base',
    'Organization',
]


class Organization(BaseTableInt):
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)
    description = sa.Column(sa.String)


class Department(BaseTableInt):
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)
    organization_id = sa.Column(sa.ForeignKey(Organization.id))
    organization = relationship('Organization')

    @property
    def organization_name(self) -> str:
        return (self.organization and self.organization.name) or ""


class Users(BaseTable):
    email = sa.Column(sa.String(255), primary_key=True)
    fullname = sa.Column(sa.String(255), nullable=False)
    department_id = sa.Column(sa.ForeignKey(Department.id))
    position = sa.Column(sa.Enum(UsersPositionEnum))
    phone = sa.Column(sa.String(255), nullable=False)
    password_hash = sa.Column(sa.String(255))
    promoted_by = sa.Column(sa.ForeignKey('users.email'), nullable=True)


class Document(BaseTableInt):
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(255))
    sender_id = sa.Column(sa.ForeignKey(Users.email))
    executor_id = sa.Column(sa.ForeignKey(Users.email))
    file_name = sa.Column(sa.String(255))
    description = sa.Column(sa.String)
    from_id = sa.Column(sa.Integer)
    to_id = sa.Column(sa.Integer)
    status = sa.Column(sa.Enum(DocumentStatusEnum))
    from_org_id = sa.Column(sa.ForeignKey(Organization.id))
    to_org_id = sa.Column(sa.ForeignKey(Organization.id))
    send_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())
    received_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())
    expiring_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())

