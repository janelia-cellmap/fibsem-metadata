import click
import uvicorn
from fastapi import APIRouter, FastAPI
from mangum import Mangum

from fibsem_metadata.api.v1.api import api_router
from fibsem_metadata.core.config import settings

app = FastAPI(title="Cellmap")
root_router = APIRouter()

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)

handler = Mangum(app, lifespan="off")

@click.command()
@click.option("--host", default="0.0.0.0", help="Host for the uvicorn server")
@click.option("--port", default=80, help="Port for the uvicorn server")
@click.option("--log_level", default="debug", help="Logging level")
@click.option("--reload", default=False, help="enable auto-reload")
def main(host: str, port: int, log_level: str, reload: bool):
    uvicorn.run(app, host=host, port=port, log_level=log_level, reload=reload)


if __name__ == "__main__":
    main()