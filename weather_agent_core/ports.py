"""Port definitions (Protocol interfaces) for external dependencies.

These Protocols define the contracts that external adapters must fulfill.
Each team implements their own adapters (e.g., Spark-based, PostgreSQL-based)
and injects them into the AgentRuntime.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass
class WeatherInfo:
    """Weather data returned by the weather database service."""

    location: str
    temperature: float  # Celsius
    humidity: float  # Percentage (0-100)
    condition: str  # e.g., "sunny", "cloudy", "rainy"


class WeatherDBService(Protocol):
    """Protocol for the weather database service.

    Any implementation must provide these two methods.
    Use the contract tests in core/tests/contract_test_weather_db.py
    to verify your implementation.
    """

    def get_today_weather(self, location: str) -> WeatherInfo:
        """Retrieve today's weather for a given location."""
        ...

    def get_user_location(self, user_id: str) -> str:
        """Retrieve the city/location name for a given user."""
        ...
