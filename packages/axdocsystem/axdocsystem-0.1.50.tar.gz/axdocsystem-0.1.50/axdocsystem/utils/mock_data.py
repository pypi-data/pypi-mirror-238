import random
from datetime import datetime, timedelta
from axdocsystem.db.schemas import DocumentStatusEnum, UsersPositionEnum
from axdocsystem.db.types import TUOWFactory
from axdocsystem.src.api.schemas import UsersPostSchema


async def create_mock_data(uowf: TUOWFactory):
    async with uowf() as uow:
        organization = await uow.repo.organization.add(
            uow.repo.organization.Schema(
                name='AxOrg',
                description='hello world',
            )
        )
        department = await uow.repo.department.add(
            uow.repo.department.Schema(
                name='AxDepartment',
                organization_id=organization.id,  # type: ignore
            )
        )
        randome_session =random.randint(111111111, 999999999) 

        sender = await uow.repo.users.add(
                UsersPostSchema(  # type: ignore
                email=f'ax0_{randome_session}@gmail.com',
                fullname='ax0',
                department_id=department.id,
                position=UsersPositionEnum.STUDENT,
                phone=str(random.randint(111111111, 999999999)),
                promoted_by=None,
            )
        )
        receiver = await uow.repo.users.add(
            UsersPostSchema(  # type: ignore
                email=f'ax1_{randome_session}@gmail.com',
                fullname='ax1',
                department_id=department.id,
                position=UsersPositionEnum.LIBRARIAN,
                phone=str(random.randint(111111111, 999999999)),
                promoted_by=None,
            )
        )

        for i in range(random.randint(50, 500)):
            await uow.repo.document.add(
                uow.repo.document.Schema(
                    title=str(random.randint(1111111111, 9999999999)),
                    sender_id=sender.email,
                    executor_id=receiver.email,
                    file_name='0.pdf',
                    file_size=0,
                    file_external_name='0.pdf',
                    content_type='Aplication/pdf',
                    description='cool',
                    status=DocumentStatusEnum.NEW,
                    from_org_id=organization.id,
                    to_org_id=organization.id,
                    send_at=datetime.now(),
                    received_at=datetime.now(),
                    expiring_at=datetime.now() - timedelta(days=random.randint(-100, 100)),
                )
            )

        await uow.save()
