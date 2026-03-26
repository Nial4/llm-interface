from core.ports import WeatherDBService, WeatherInfo
from core.runtime import AgentRuntime, LLMConfig, ObservabilityConfig

# Lazy import — WeatherAgent requires langchain at runtime
def __getattr__(name: str):
    if name == "WeatherAgent":
        from core.agent import WeatherAgent
        return WeatherAgent
    raise AttributeError(f"module 'core' has no attribute {name!r}")

__all__ = [
    "WeatherDBService",
    "WeatherInfo",
    "AgentRuntime",
    "LLMConfig",
    "ObservabilityConfig",
    "WeatherAgent",
]
