from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


# 代表应用的配置设置，包含API密钥、端点URL、研究参数等
class Settings(BaseSettings):
    tavily_api_key: str

    azure_openai_api_key: str
    azure_openai_endpoint: str
    azure_openai_deployment: str

    research_max_results: int = 3
    fetch_max_chars: int = 8000
    summary_max_input_chars: int = 6000
    article_fetch_timeout_seconds: float = 10.0
    article_min_length: int = 200
    max_article_concurrency: int = 3

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def azure_openai_base_url(self) -> str:
        return f"{self.azure_openai_endpoint.rstrip('/')}/openai/v1/"


# 使用lru_cache装饰器缓存设置实例，确保全局只创建一个Settings对象
@lru_cache
def get_settings() -> Settings:
    return Settings()  # pyright: ignore[reportCallIssue]
