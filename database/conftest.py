from typing import Any
from configs import configs
import pytest


@pytest.fixture()
def connection_string(request: Any) -> str:
    return configs["db_conn"]
