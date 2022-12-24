import io
import zipfile

import asyncpg
import ormar
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile
from starlette.responses import FileResponse, StreamingResponse

from api.users import get_current_active_user
from config import config
from models import File, User

router = APIRouter(
    prefix='/files',
    tags=['files'],
)

FileSchema = File.get_pydantic(exclude={'user'})


@router.post('', response_model=FileSchema)
async def create_file(
    file: UploadFile,
    path: str = Form(default=''),
    user: User = Depends(get_current_active_user),
):
    user_dir = config.media_dir / str(user.id)
    path = (user_dir / path.removeprefix('/')).resolve()
    if not path.suffix:
        path /= file.filename

    if not path.is_relative_to(user_dir):
        raise HTTPException(
            status_code=400, detail='Path must be inside root dir'
        )

    content = await file.read()
    try:
        saved_file = await File.objects.create(
            name=file.filename,
            size=len(content),
            path=path.relative_to(user_dir).as_posix(),
            user=user,
        )
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=409, detail='File already exists')

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return saved_file


@router.get('', response_model=list[FileSchema])
async def get_files(user: User = Depends(get_current_active_user)):
    return await user.files.all()


@router.get('/{path_or_id:path}')
async def get_file_by_path(
    path_or_id: str, user: User = Depends(get_current_active_user)
):
    if path_or_id.isnumeric():
        try:
            file = await File.objects.get(id=int(path_or_id))
            return FileResponse(config.media_dir / str(user.id) / file.path)
        except ormar.NoMatch:
            raise HTTPException(status_code=404, detail='File not found')

    path = (config.media_dir / str(user.id) / path_or_id).resolve()
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
