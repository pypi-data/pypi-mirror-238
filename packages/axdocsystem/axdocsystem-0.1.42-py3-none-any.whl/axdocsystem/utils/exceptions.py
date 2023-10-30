from typing import Optional
from fastapi import HTTPException, status


class ContentSizeExceeded(HTTPException):
    STATUS_CODE = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE

    def __init__(self, detail: str) -> None:
        super().__init__(self.STATUS_CODE, detail=detail, headers={})


class UnsupportedContentType(HTTPException):
    STATUS_CODE = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    DETAIL = "`{}` is unsupported content type"

    def __init__(self, got_type: Optional[str] = None) -> None:
        got_type = got_type or 'unknown'
        detail = self.DETAIL.format(got_type)
        super().__init__(self.STATUS_CODE, detail=detail, headers={})

