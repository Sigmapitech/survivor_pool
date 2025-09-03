import logging
import sys
from functools import lru_cache

from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__package__)


class Settings(BaseSettings):
    log_level: str = "INFO"
    development_mode: bool = "dev" in sys.argv
    model_config = SettingsConfigDict(
        env_file=".env.dev" if "dev" in sys.argv else ".env.prod"
    )

    jeb_api_url: str
    jeb_api_auth: str
    jwt_secret: str

    mail_user: str
    mail_pass: str

    def configure_logging(self):
        logging.basicConfig(level=self.log_level.upper())
        logging.info(f"Logging level set to {self.log_level}")


try:
    settings = lru_cache(maxsize=1)(Settings)()


except ValidationError as e:
    raise e


settings.configure_logging()

__all__ = ("settings",)
