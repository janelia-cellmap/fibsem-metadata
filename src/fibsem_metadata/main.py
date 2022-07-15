from fastapi import APIRouter, FastAPI
from fibsem_metadata.api.v1.api import api_router
from fibsem_metadata.core.config import settings
import click
from mangum import Mangum
import uvicorn

app = FastAPI(title="Cellmap")
root_router = APIRouter()

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)

handler = Mangum(app, lifespan='off')

@click.command()
@click.option('--host', default='0.0.0.0', help='Host for the uvicorn server')
@click.option('--port', default=8001, help='Port for the uvicorn server')
@click.option('--log_level', default='debug', help='Logging level')
@click.option('--reload', default=False, help='enable auto-reload')
def main_cli(host: str,
             port: int,
             log_level: str,
             reload: bool):

    uvicorn.run(app,
                host=host,
                port=port,
                log_level=log_level,
                reload=reload)


if __name__ == "__main__":
    main_cli()
