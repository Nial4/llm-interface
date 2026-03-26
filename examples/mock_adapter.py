"""Mock adapter for local demo and testing.

This adapter uses in-memory dicts to simulate a weather database.
It serves two purposes:
1. A runnable demo without any real database
2. A reference implementation showing how to satisfy the WeatherDBService Protocol
"""

from __future__ import annotations

from core.ports import WeatherDBService, WeatherInfo


class MockWeatherDB:
    """In-memory mock implementation of WeatherDBService."""

    def __init__(self) -> None:
        self._users: dict[str, str] = {
            "u001": "Tokyo",
            "u002": "Osaka",
            "u003": "New York",
        }
        self._weather: dict[str, WeatherInfo] = {
            "Tokyo": WeatherInfo(
                location="Tokyo",
                temperature=22.5,
                humidity=60.0,
                condition="sunny",
            ),
            "Osaka": WeatherInfo(
                location="Osaka",
                temperature=24.0,
                humidity=70.0,
                condition="cloudy",
            ),
            "New York": WeatherInfo(
                location="New York",
                temperature=15.0,
                humidity=55.0,
                condition="rainy",
            ),
        }

    def get_user_location(self, user_id: str) -> str:
        if user_id not in self._users:
            raise KeyError(f"User not found: {user_id}")
        return self._users[user_id]

    def get_today_weather(self, location: str) -> WeatherInfo:
        if location not in self._weather:
            raise KeyError(f"Weather data not found for location: {location}")
        return self._weather[location]


# Type check: MockWeatherDB satisfies WeatherDBService Protocol
_check: WeatherDBService = MockWeatherDB()
