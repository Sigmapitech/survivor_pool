import logging
import sys
from functools import lru_cache
from typing import Sequence, cast

from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__package__)


def join_with_seps(parts: Sequence[str], separators: Sequence[str]) -> str:
    result = parts[0]

    for i, sep in enumerate(separators):
        result += sep + parts[i + 1]
    return result


class Settings(BaseSettings):
    db_host: str | None = None
    db_port: str | None = None

    db_user: str | None = None
    db_password: str | None = None

    db_name: str
    db_connect_args: dict[str, str | bool] = {}
    db_protocol: str = "mariadb+pymysql"

    log_level: str = "INFO"
    development_mode: bool = "dev" in sys.argv
    model_config = SettingsConfigDict(
        env_file=".env.dev" if "dev" in sys.argv else ".env.prod"
    )

    @property
    def database_url(self) -> str:
        # TODO: rewrite this parser
        distant_specifiers = (
            self.db_host,
            self.db_user,
            self.db_password,
            self.db_port,
        )

        if all(x is None for x in distant_specifiers):
            return ":///".join((self.db_protocol, self.db_name))

        if any(x is None for x in distant_specifiers):
            raise ValueError("Distant specifiers must all be set or None")

        return join_with_seps(
            cast(
                tuple[str, ...],
                (
                    self.db_protocol,
                    self.db_user,
                    self.db_password,
                    self.db_host,
                    self.db_port,
                    self.db_name,
                ),
            ),
            ("://", ":", "@", ":", "/"),
        )

    def configure_logging(self):
        logging.basicConfig(level=self.log_level.upper())
        logging.info(f"Logging level set to {self.log_level}")


try:
    settings = lru_cache(maxsize=1)(Settings)()


except ValidationError as e:
    raise e


settings.configure_logging()

__all__ = ("settings",)
