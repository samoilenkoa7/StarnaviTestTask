from pydantic import BaseSettings


class Settings(BaseSettings):
    # server settings

    database_url: str = 'postgresql+asyncpg://postgres:postgres@db:5432/postgres'
    server_host: str = '127.0.0.1'
    server_port: int = 8000

    # jwt settings

    jwt_secret: str = 'RvDN2wymzgAYfWgpYuky33gOAIoWUjtFZkeoq-1kYyE'
    jwt_algorithm: str = 'HS256'
    jwt_expiration: int = 100000  # seconds


settings = Settings(
    _env_file='~/Documents/StarnaviTestTasl/.env',
    _env_file_encoding='utf-8',
)
