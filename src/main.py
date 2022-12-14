import aiohttp
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination

from api.router import router
from config import config
from models import database

app = FastAPI(
    title=config.project_name,
    default_response_class=ORJSONResponse,
)

session = aiohttp.ClientSession()
app.include_router(router)
add_pagination(app)


@app.on_event('startup')
async def startup() -> None:
    if not database.is_connected:
        await database.connect()


@app.on_event('shutdown')
async def shutdown() -> None:
    if database.is_connected:
        await database.disconnect()

    await session.close()


if __name__ == '__main__':
    uvicorn.run('main:app', host=config.host, port=config.port)
