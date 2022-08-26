import click
import uvicorn
from fastapi import APIRouter, FastAPI
from mangum import Mangum
from fibsem_metadata.api.v1.api import api_router
from fibsem_metadata.core.config import settings
from typing import Dict


app = FastAPI(title="Cellmap")
root_router = APIRouter()


@root_router.get('/health')
def api_status() -> Dict[str, bool]:
    from fibsem_metadata.db.session import engine
    from sqlalchemy.exc import OperationalError
    import fibsem_metadata
    try:
        engine.connect()
        connected = True
    except OperationalError:
        connected = False

    return {'database_connected': connected, 'version': fibsem_metadata.__version__}


app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)

handler = Mangum(app, lifespan="off")

@click.command()
@click.option("--host", default="0.0.0.0", help="Host for the uvicorn server")
@click.option("--port", default=80, help="Port for the uvicorn server")
@click.option("--log_level", default="debug", help="Logging level")
@click.option("--reload", default=False, help="enable auto-reload")
def main(host: str, port: int, log_level: str, reload: bool):
    uvicorn.run("main:app", host=host, port=port, log_level=log_level, reload=reload)


if __name__ == "__main__":
    main()
