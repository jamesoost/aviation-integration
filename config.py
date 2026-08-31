import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class PipelineConfig:
    engine: str
    raw_dir: str
    staging_dir: str
    quarantine_dir: str
    processed_dir: str
    logs_dir: str
    db_path: str
    api_limit: int
    api_offset: int
    api_timeout: int


def load_config() -> PipelineConfig:
    load_dotenv()

    processed_dir = os.getenv("PROCESSED_DIR", "data/processed")

    return PipelineConfig(
        engine=os.getenv("ETL_ENGINE", "pandas").strip().lower(),
        raw_dir=os.getenv("RAW_DIR", "data/raw"),
        staging_dir=os.getenv("STAGING_DIR", "data/staging"),
        quarantine_dir=os.getenv("QUARANTINE_DIR", "data/quarantine"),
        processed_dir=processed_dir,
        logs_dir=os.getenv("LOGS_DIR", "data/logs"),
        db_path=os.getenv("DB_PATH", f"{processed_dir}/aviation.db"),
        api_limit=int(os.getenv("API_LIMIT", "10")),
        api_offset=int(os.getenv("API_OFFSET", "0")),
        api_timeout=int(os.getenv("API_TIMEOUT", "10")),
    )
