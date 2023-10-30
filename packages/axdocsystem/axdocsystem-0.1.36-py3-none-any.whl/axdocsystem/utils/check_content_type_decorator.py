from typing import Iterable, Optional
from fastapi import UploadFile
from .exceptions import UnsupportedContentType


DEFAULT_ALLOWED_CONTENT_TYPES = (
    "text/plain",
    "text/plain; charset=utf-8",
    "application/pdf",
    "application/msword",
    (
        "application/vnd.openxmlformats"
        "-officedocument.wordprocessingml.document"
    )
)


def get_content_type_checker(
    allowed_content_types: Iterable = DEFAULT_ALLOWED_CONTENT_TYPES,
    allow_empty_content_type: bool = False,
):
    def checker(file: Optional[UploadFile] = None):
        content_type = file.content_type if file else None

        if not content_type:
            if not allow_empty_content_type:
                raise UnsupportedContentType(content_type)
        elif not content_type in allowed_content_types: 
            raise UnsupportedContentType(content_type)

    return checker 

