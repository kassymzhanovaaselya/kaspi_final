from typing import Type, Any

import pytest

from database.database import Database


@pytest.fixture()
def connection_string(request: Any) -> str:
    return "dbname=postgres port=5432 user=postgres password=postgres host=localhost"
