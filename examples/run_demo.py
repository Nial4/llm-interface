"""End-to-end demo of the Weather Agent Core.

Run:
    python -m examples.run_demo

This demonstrates how a team would:
1. Implement a WeatherDBService adapter (here using MockWeatherDB)
2. Configure LLM and observability settings
3. Create and invoke the WeatherAgent
"""

from core import AgentRuntime, LLMConfig, ObservabilityConfig, WeatherAgent
from examples.mock_adapter import MockWeatherDB


def main() -> None:
    # 1. Each team provides their own adapter
    weather_db = MockWeatherDB()

    # 2. Configure (each team may use different config values)
    runtime = AgentRuntime(
        weather_db=weather_db,
        llm_config=LLMConfig(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            region_name="ap-northeast-1",
            credentials_profile_name="your-aws-profile",
        ),
        observability=ObservabilityConfig(
            enabled=False,  # Disable MLflow for this demo
        ),
    )

    # 3. Create agent and invoke
    agent = WeatherAgent(runtime)
    response = agent.invoke(
        user_id="u001",
        user_input="今日の天気はどうですか？傘は必要ですか？",
    )

    print("=== Weather Agent Response ===")
    print(response)


if __name__ == "__main__":
    main()
