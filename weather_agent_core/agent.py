"""WeatherAgent — the core agent logic.

This module is the heart of the Core library. It orchestrates:
1. Fetching user location and weather data via the injected WeatherDBService
2. Building a prompt from the template + fetched data
3. Calling the LLM (Bedrock) to generate a weather report
4. (Optionally) tracing the entire flow with MLflow
"""

from __future__ import annotations

from pathlib import Path

import yaml
from langchain_core.messages import HumanMessage, SystemMessage

from weather_agent_core.llm import create_llm
from weather_agent_core.runtime import AgentRuntime

_PROMPTS_DIR = Path(__file__).parent / "prompts"


def _load_prompt_template() -> str:
    with open(_PROMPTS_DIR / "weather.yaml") as f:
        return yaml.safe_load(f)["system"]


def _setup_observability(config) -> None:
    """Configure MLflow tracking if enabled."""
    if not config.enabled:
        return

    import mlflow

    if config.tracking_uri:
        mlflow.set_tracking_uri(config.tracking_uri)
    mlflow.set_experiment(config.experiment_name)

    if config.extra_tags:
        mlflow.set_tags(config.extra_tags)


class WeatherAgent:
    """Minimal weather agent that fetches data, builds a prompt, and calls an LLM.

    Usage::

        runtime = AgentRuntime(weather_db=my_db_adapter)
        agent = WeatherAgent(runtime)
        report = agent.invoke(user_id="u001", user_input="今日の天気はどうですか")
    """

    def __init__(self, runtime: AgentRuntime) -> None:
        self._runtime = runtime
        self._llm = create_llm(runtime.llm_config)
        self._prompt_template = _load_prompt_template()
        _setup_observability(runtime.observability)

    def invoke(self, user_id: str, user_input: str) -> str:
        """Run the agent: fetch context, call LLM, return the response."""
        if self._runtime.observability.enabled:
            return self._invoke_with_trace(user_id, user_input)
        return self._invoke_core(user_id, user_input)

    def _invoke_with_trace(self, user_id: str, user_input: str) -> str:
        import mlflow

        @mlflow.trace(name="WeatherAgent.invoke")
        def _traced(user_id: str, user_input: str) -> str:
            return self._invoke_core(user_id, user_input)

        return _traced(user_id, user_input)

    def _invoke_core(self, user_id: str, user_input: str) -> str:
        db = self._runtime.weather_db

        # Step 1: Fetch user location
        location = db.get_user_location(user_id)

        # Step 2: Fetch weather data
        weather = db.get_today_weather(location)

        # Step 3: Build prompt
        system_prompt = self._prompt_template.format(
            location=weather.location,
            condition=weather.condition,
            temperature=weather.temperature,
            humidity=weather.humidity,
        )

        # Step 4: Call LLM
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_input),
        ]
        response = self._llm.invoke(messages)

        return response.content
