from axabc.db import BaseRepoCollector
from . import repository as repo


class RepoCollection(BaseRepoCollector):
    organization: repo.OrganizationRepository
    department: repo.DepartmentRepository
    users: repo.UsersRepository
    document: repo.DocumentRepository

