# app/Utils/file_uploader.py
import os
import aiofiles
from fastapi import UploadFile

class FileUploader:
    _dir = "uploads"

    @classmethod
    async def upload(cls, file: UploadFile | None, prefix: str) -> str | None:
        if not file:
            return None
        os.makedirs(cls._dir, exist_ok=True)
        ext      = file.filename.split(".")[-1]
        filename = f"{prefix}_{file.filename}"
        path     = os.path.join(cls._dir, filename)

        # aiofiles is non-blocking — doesn't freeze the event loop
        async with aiofiles.open(path, "wb") as f:
            content = await file.read()
            await f.write(content)

        return path