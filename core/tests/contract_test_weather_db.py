"""Contract tests for WeatherDBService implementations.

Any team implementing a WeatherDBService adapter MUST subclass this test
and provide a concrete fixture. Running these tests guarantees that the
adapter behaves consistently with what the Core agent expects.

Usage example (for a PostgreSQL adapter)::

    # tests/test_postgres_adapter.py
    from core.tests.contract_test_weather_db import WeatherDBServiceContractTest
    from my_adapters.postgres import PostgresWeatherDB

    class TestPostgresWeatherDB(WeatherDBServiceContractTest):
        @pytest.fixture()
        def weather_db(self):
            db = PostgresWeatherDB(dsn="postgresql://localhost/test")
            db.seed_test_data()  # insert known test rows
            yield db
            db.cleanup()

        @pytest.fixture()
        def known_user_id(self):
            return "test-user-001"

        @pytest.fixture()
        def known_location(self):
            return "Tokyo"
"""

from __future__ import annotations

import pytest

from core.ports import WeatherDBService, WeatherInfo


class WeatherDBServiceContractTest:
    """Base contract test suite — subclass and provide fixtures to use.

    Required fixtures (must be implemented by subclass):
        weather_db   — a concrete WeatherDBService instance with test data
        known_user_id — a user_id that exists in the test data
        known_location — a location that exists in the test data
    """

    # ------------------------------------------------------------------
    # Fixtures to be overridden
    # ------------------------------------------------------------------

    @pytest.fixture()
    def weather_db(self) -> WeatherDBService:
        raise NotImplementedError("Subclass must provide a weather_db fixture")

    @pytest.fixture()
    def known_user_id(self) -> str:
        raise NotImplementedError("Subclass must provide a known_user_id fixture")

    @pytest.fixture()
    def known_location(self) -> str:
        raise NotImplementedError("Subclass must provide a known_location fixture")

    # ------------------------------------------------------------------
    # Contract: get_user_location
    # ------------------------------------------------------------------

    def test_get_user_location_returns_string(self, weather_db, known_user_id):
        location = weather_db.get_user_location(known_user_id)
        assert isinstance(location, str)
        assert len(location) > 0

    def test_get_user_location_unknown_user_raises(self, weather_db):
        with pytest.raises(Exception):
            weather_db.get_user_location("__nonexistent_user_id__")

    # ------------------------------------------------------------------
    # Contract: get_today_weather
    # ------------------------------------------------------------------

    def test_get_today_weather_returns_weather_info(self, weather_db, known_location):
        weather = weather_db.get_today_weather(known_location)
        assert isinstance(weather, WeatherInfo)

    def test_weather_info_has_required_fields(self, weather_db, known_location):
        weather = weather_db.get_today_weather(known_location)
        assert isinstance(weather.location, str) and len(weather.location) > 0
        assert isinstance(weather.temperature, (int, float))
        assert isinstance(weather.humidity, (int, float))
        assert 0 <= weather.humidity <= 100
        assert isinstance(weather.condition, str) and len(weather.condition) > 0

    def test_get_today_weather_unknown_location_raises(self, weather_db):
        with pytest.raises(Exception):
            weather_db.get_today_weather("__nonexistent_location__")
