"""Runtime configuration and dependency container for the Weather Agent."""

from __future__ import annotations

from dataclasses import dataclass, field

from core.ports import WeatherDBService


@dataclass
class LLMConfig:
    """Configuration for the LLM provider (Bedrock).

    This is a config-level dependency, not a Protocol —
    the LLM client is managed internally by Core.
    """

    model_id: str = "anthropic.claude-sonnet-4-20250514"
    region_name: str = "us-east-1"
    credentials_profile_name: str | None = None
    temperature: float = 0.3
    max_tokens: int = 1024


@dataclass
class ObservabilityConfig:
    """Configuration for MLflow tracing.

    This is a config-level dependency — Core owns the tracing logic,
    each team only provides connection details.
    """

    tracking_uri: str = ""
    experiment_name: str = "weather-agent"
    enabled: bool = True
    extra_tags: dict[str, str] = field(default_factory=dict)


@dataclass
class AgentRuntime:
    """Central dependency container injected into the WeatherAgent.

    - weather_db: Protocol — must be implemented and injected by each team.
    - llm_config: Config — controls LLM behavior, managed by Core.
    - observability: Config — controls tracing destination, managed by Core.
    """

    weather_db: WeatherDBService
    llm_config: LLMConfig = field(default_factory=LLMConfig)
    observability: ObservabilityConfig = field(default_factory=ObservabilityConfig)
