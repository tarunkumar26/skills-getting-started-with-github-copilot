from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module

ORIGINAL_ACTIVITIES = deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities(monkeypatch):
    fresh_activities = deepcopy(ORIGINAL_ACTIVITIES)
    monkeypatch.setattr(app_module, "activities", fresh_activities)


@pytest.fixture
def client():
    return TestClient(app_module.app)
