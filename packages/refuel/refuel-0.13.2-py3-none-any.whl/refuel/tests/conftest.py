import pytest
import os
import refuel


@pytest.fixture
def refuel_client():
    options = {"api_key": os.environ.get("REFUEL_TEST_API_KEY")}
    return refuel.init(**options)


@pytest.fixture
def refuel_client_with_project():
    options = {
        "api_key": os.environ.get("REFUEL_TEST_API_KEY"),
        "project": "test_sdk",
    }
    return refuel.init(**options)
