import pathlib
from typing import Any, List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator

# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_HOST: str = 'localhost'
    DB_USER: str = 'postgres'
    DB_PORT: int = 5432
    DB_NAME: str = 'fibsem_metadata'
    DB_PASSWORD: str = 'admin'

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://openorganelle.org",
        "http://localhost",
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
        cls: Any, v: Union[str, List[str]]
    ) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    SQLALCHEMY_DATABASE_URI: str = (
        "postgresql://admin:admin@localhost:5432/fibsem_metadata"
    )

    class Config:
        case_sensitive = True


settings = Settings()
