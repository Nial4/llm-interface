"""Contract test run against the MockWeatherDB adapter.

This demonstrates how each team would verify their adapter
satisfies the WeatherDBService contract.
"""

import pytest

from core.tests.contract_test_weather_db import WeatherDBServiceContractTest
from examples.mock_adapter import MockWeatherDB


class TestMockWeatherDB(WeatherDBServiceContractTest):

    @pytest.fixture()
    def weather_db(self):
        return MockWeatherDB()

    @pytest.fixture()
    def known_user_id(self):
        return "u001"

    @pytest.fixture()
    def known_location(self):
        return "Tokyo"
