from typing import Any, List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator
from .aws import on_lambda, get_database_secret, AWS_DB_SECRET_NAME

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_TYPE: str = 'postgresql'
    DB_HOST: str = 'localhost'
    DB_USER: str = 'postgres'
    DB_PORT: int = 5432
    DB_NAME: str = 'cellmap'
    DB_PASSWORD: str = 'admin'

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://openorganelle.org",
        "http://localhost",
    ]

    def db_uri(self) -> str:
        return f'{self.DB_TYPE}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{settings.DB_PORT}/{self.DB_NAME}'

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
        cls: Any, v: Union[str, List[str]]
    ) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True


if on_lambda():
    # if running on aws lambda, check for a secret name environment variable
    db_secret = get_database_secret()
    if db_secret is None:
        raise EnvironmentError(f'This program is running in aws lambda, but the required environment variable {AWS_DB_SECRET_NAME} could not be found')
    settings = Settings(DB_PASSWORD=db_secret['password'])
else:
    settings = Settings()
