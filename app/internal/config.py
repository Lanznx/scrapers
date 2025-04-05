# app/internal/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "LinkedIn Job Scraper"
    debug: bool = False
    scraper_slow_mo: float = 1.3
    scraper_max_workers: int = 1
    scraper_timeout: int = 40
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        env_file = ".env"


settings = Settings()
