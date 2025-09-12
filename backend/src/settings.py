from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent  # epi-registry/backend


class JSONDataConfig(BaseModel):
    data_dir: Path = BASE_DIR / "src" / "data"

    # Raw data
    drugs_filename: str = "drugs.json"
    modifiers_filename: str = "modifiers.json"
    seizure_types_filename: str = "seizure_types.json"

    seizure_drug_map_filename: str = "seizure_drug_map.json"
    modifier_rules_filename: str = "modifier_rules.json"


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    asm: str = "/asm"


class APIConfig(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class DatabaseConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    name: str
    provider: str = "postgresql+asyncpg"

    @property
    def dsn(self) -> str:
        return f"{self.provider}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        env_file=(BASE_DIR / ".env"),
        extra="ignore",
    )
    base_dir: Path = BASE_DIR
    json_data: JSONDataConfig = JSONDataConfig()
    debug: bool
    cors_origins: list[str]
    run: RunConfig = RunConfig()
    api: APIConfig = APIConfig()
    db: DatabaseConfig


settings = Settings()
