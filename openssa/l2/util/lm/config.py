"""
==================================
LANGUAGE MODEL (LM) CONFIGURATIONS
==================================
"""


import os

from dotenv import load_dotenv


load_dotenv(override=True)


class LMConfig:
    """
    Configuration class for language models, secret keys, and default values.
    Can be overridden by user setting LMConfig.<attribute>.
    """

    # Llama LMs
    LLAMA_API_KEY: str | None = os.environ.get("LLAMA_API_KEY")
    LLAMA_API_URL: str = os.environ.get("LLAMA_API_URL", "https://api.llama-api.com")
    DEFAULT_LLAMA_MODEL: str = "llama3-70b"

    # OpenAI LMs
    OPENAI_API_KEY: str | None = os.environ.get("OPENAI_API_KEY")
    OPENAI_API_URL: str = os.environ.get("OPENAI_API_URL", "https://api.openai.com/v1")
    DEFAULT_OPENAI_MODEL: str = "gpt-4o"  # platform.openai.com/docs/models/gpt-4o
    DEFAULT_SMALL_OPENAI_MODEL: str = "gpt-4o-mini"  # platform.openai.com/docs/models/gpt-4o-mini

    # LM parameters
    DEFAULT_SEED: int = 7 * 17 * 14717
    DEFAULT_TEMPERATURE: float = 0.0
