from enum import Enum


class DocumentStatusEnum(Enum):
    NEW = 'new'
    SUCCESS = 'success'


class UsersPositionEnum(Enum):
    STUDENT = 1
    PROFESSOR = 2
    ADMINISTRATOR = 3
    LIBRARIAN = 4
    RESEARCHER = 5
    DEAN = 6
    CHAIRPERSON = 7
    JANITOR = 8

