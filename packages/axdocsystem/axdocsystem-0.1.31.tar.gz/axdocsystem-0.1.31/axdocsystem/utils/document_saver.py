import os
import shutil
from typing import Optional
import aiofiles
from uuid import uuid4
from fastapi import UploadFile


class DocumentSaver:
    _DOCS_DIR = 'documents'

    async def save_document(self, id: Optional[str], file: UploadFile):
        _, ext = os.path.splitext(str(file.filename))
        newname = f"{str(id)}{ext}"
        path = f"{self._DOCS_DIR}/{newname}"

        if os.path.exists(path):
           old_doc_new_path = f"{self._DOCS_DIR}/{str(id)}-{str(uuid4())}{ext}"
           shutil.move(path, old_doc_new_path)

        async with aiofiles.open(path, "wb") as f:
            rode = await file.read()
            size = len(rode)
            await f.write(rode)

        return newname, size

    async def get_bytes(self, filename):
        async with aiofiles.open(f"{self._DOCS_DIR}/{filename}", "rb") as f:
            return await f.read()

