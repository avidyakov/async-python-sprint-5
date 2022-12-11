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

app.include_router(router.router)
add_pagination(app)


@app.on_event('startup')
async def startup() -> None:
    # database_ = app.state.database
    if not database.is_connected:
        await database.connect()


@app.on_event('shutdown')
async def shutdown() -> None:
    # database_ = app.state.database
    if database.is_connected:
        await database.disconnect()


if __name__ == '__main__':
    uvicorn.run('main:app', host=config.host, port=config.port)
