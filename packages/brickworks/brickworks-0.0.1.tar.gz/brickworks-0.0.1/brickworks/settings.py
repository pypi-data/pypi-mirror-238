from pydantic_settings import BaseSettings


class BrickworksSettings(BaseSettings):
    app_name: str = "Adamantium API"

    DB_USE_SQLITE: bool = True
    DB_HOST: str = "127.0.0.1:5432"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = ""
    DB_NAME: str = "postgres"

    bricks: list[str] = ["brickworks.auth"]
