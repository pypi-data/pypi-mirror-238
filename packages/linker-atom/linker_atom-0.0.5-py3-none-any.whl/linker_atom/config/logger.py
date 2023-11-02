from pydantic import BaseModel, Field


class LoggerConfig(BaseModel):
    log_backup_count: int = Field(default=30, env="LOG_BACKUP_COUNT")
    log_dir: str = Field(default="atom", env="LOG_DIR")
