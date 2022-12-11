from fastapi import APIRouter, Form, UploadFile

from models import File

router = APIRouter(
    prefix='/files',
    tags=['files'],
)


@router.post('', response_model=File)
async def create_file(file: UploadFile, path: str | None = Form()):
    file = await File.objects.create(
        name=file.filename,
        size=len(file.file.read()),
        path=path,
    )
    return file


@router.get('', response_model=list[File])
async def get_files():
    files = await File.objects.all()
    return files
