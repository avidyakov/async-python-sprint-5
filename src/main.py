import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination

from api import router
from config import config
from models import database

app = FastAPI(
    title=config.project_name,
    default_response_class=ORJSONResponse,
)
app.state.database = database

app.include_router(router.router)
add_pagination(app)


if __name__ == '__main__':
    uvicorn.run('main:app', host=config.host, port=config.port)
