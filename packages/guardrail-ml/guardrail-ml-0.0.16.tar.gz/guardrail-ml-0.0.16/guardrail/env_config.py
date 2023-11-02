import pydantic 
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()

class GuardrailEnvConfig(BaseSettings, frozen=True):
    """Environment configurations for Guardrail"""

    guardrail_api_key: str = pydantic.Field(
        default="",
        env="GUARDRAIL_API_KEY",
        description="API key for Guardrail ML"
    )

    openai_api_key: str = pydantic.Field(
        default="",
        env="OPENAI_API_KEY",
        description="API key for OpenAI"
    )

    serper_api_key: str = pydantic.Field(
        default="",
        env="SERPER_API_KEY",
        description="API Key for Serper",
    )

    scraper_api_key: str = pydantic.Field(
        default="",
        env="SCRAPER_API_KEY",
        description="API Key for Scraper",
    )

    perspective_api_key: str = pydantic.Field(
        default="",
        env="PERSPECTIVE_API_KEY",
        description="API Key for Perspective",
    )

guardrail_env_config = GuardrailEnvConfig()