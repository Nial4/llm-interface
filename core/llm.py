"""LLM factory — creates a ChatBedrock instance from config.

This is centralized in Core so that both teams use the same LLM client.
"""

from langchain_aws import ChatBedrock
from langchain_core.language_models import BaseChatModel

from core.runtime import LLMConfig


def create_llm(config: LLMConfig) -> BaseChatModel:
    """Create a LangChain ChatModel backed by Amazon Bedrock."""
    kwargs: dict = {
        "model_id": config.model_id,
        "region_name": config.region_name,
        "model_kwargs": {
            "temperature": config.temperature,
            "max_tokens": config.max_tokens,
        },
    }
    if config.credentials_profile_name:
        kwargs["credentials_profile_name"] = config.credentials_profile_name
    return ChatBedrock(**kwargs)
