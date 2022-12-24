import io
import zipfile
from pathlib import Path

import asyncpg
import ormar
from fastapi import APIRouter, Form, HTTPException, UploadFile
from starlette.responses import FileResponse, StreamingResponse

from config import config
from models import File

router = APIRouter(
    prefix='/files',
    tags=['files'],
)


@router.post('', response_model=File)
async def create_file(file: UploadFile, path: str = Form(default='')):
    path = (config.media_dir / path.removeprefix('/')).resolve()
    if not path.suffix:
        path /= file.filename

    if not path.is_relative_to(config.media_dir):
        raise HTTPException(
            status_code=400, detail='Path must be inside root dir'
        )

    content = await file.read()
    try:
        saved_file = await File.objects.create(
            name=file.filename,
            size=len(content),
            path=path.relative_to(config.media_dir).as_posix(),
        )
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=409, detail='File already exists')

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return saved_file


@router.get('', response_model=list[File])
async def get_files():
    return await File.objects.all()


@router.get('/{path_or_id:path}')
async def get_file_by_path(path_or_id: str):
    if path_or_id.isnumeric():
        try:
            file = await File.objects.get(id=int(path_or_id))
            return FileResponse(config.media_dir / file.path)
        except ormar.NoMatch:
            raise HTTPException(status_code=404, detail='File not found')

    path = (config.media_dir / path_or_id).resolve()
    if path.is_file():
        return FileResponse(path)

    if path.is_dir():
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for file in path.iterdir():
                zip_file.write(file, file.relative_to(path))

        zip_buffer.seek(0)
        return StreamingResponse(zip_buffer, media_type='application/zip')

    raise HTTPException(status_code=404, detail='Files not found')
