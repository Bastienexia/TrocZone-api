from pydantic import AnyHttpUrl, BaseSettings
from redis.client import Redis


class Settings(BaseSettings):
    ENVIRONMENT: str = "local"
    API_URL: str = "http://localhost:8000"
    FRONT_URL: str = "http://localhost:3000"

    ACCESS_TOKEN_EXPIRE_MIUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 7 * 24 * 60

    SIGNUP_SECRET_KEY: str = "xCVM5vSEdzn-UW5Hqlaw6lqwSkU6tzr9pD6ERuQnsUY="
    SECRET_KEY: str = "QFaSkxxxBtePBn2YemwHccaIetzARBZjMWenhGrQ-pE"

    BACKEND_CORS_ORIGIN: list[AnyHttpUrl] = ["http://localhost:3000"]

    SQLALCHEMY_DATABASE_URI: str = (
        "postgresql+asyncpg://postgres:root@localhost:5433/troczone"
    )

    REDIS_HOST: str = "localhost"
    REDIS_DB: int = 1

    REDIS_PASSWORD: str | None = None


settings = Settings()

redis = Redis(
    host=settings.REDIS_HOST, db=settings.REDIS_DB, password=settings.REDIS_PASSWORD
)
