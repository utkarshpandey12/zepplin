from pydantic import Field
from pydantic_settings import BaseSettings


class ApiClientConfig(BaseSettings):
    """Configuration class"""

    MAX_REQUESTS: int = Field(
        default=300,
        env="MAX_REQUESTS",
        description="max api requests allowed before sleep",
    )

    MAX_REQUESTS_PER_MINUTES: int = Field(
        default=300,
        env="MAX_REQUESTS_PER_MINUTES",
        description="max rpm allowed before sleep",
    )
