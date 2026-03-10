from openai import AzureOpenAI
from app.config import get_settings

settings = get_settings()

client = AzureOpenAI(
    api_key=settings.azure_openai_api_key,
    azure_endpoint=settings.azure_openai_endpoint,
    api_version="2024-02-01"
)