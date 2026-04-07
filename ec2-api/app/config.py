from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4-20250514"
    # Comma-separated API keys for X-API-Key header
    api_keys: str = ""
    # Directory containing SKILL.md (default: ec2-api/skill relative to cwd)
    skill_dir: Path = Path(__file__).resolve().parent.parent / "skill"
    max_output_tokens: int = 4096
    public_url: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()


def parse_api_key_set(raw: str) -> set[str]:
    if not raw.strip():
        return set()
    return {k.strip() for k in raw.split(",") if k.strip()}
