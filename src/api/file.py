from pathlib import Path

from fastapi import APIRouter, Form, HTTPException, UploadFile

from config import config
from models import File

router = APIRouter(
    prefix='/files',
    tags=['files'],
)


@router.post('', response_model=File)
async def create_file(file: UploadFile, path: Path = Form(default='./')):
    if path.is_absolute():
        raise HTTPException(status_code=400, detail='Path must be relative')

    path = (config.media_dir / path / file.filename).resolve()
    if not path.is_relative_to(config.media_dir):
        raise HTTPException(
            status_code=400, detail='Path must be inside root dir'
        )

    content = await file.read()
    saved_file = await File.objects.create(
        name=file.filename,
        size=len(content),
        path=path.relative_to(config.media_dir).as_posix(),
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return saved_file


@router.get('', response_model=list[File])
async def get_files():
    files = await File.objects.all()
    return files
