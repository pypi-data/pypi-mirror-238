"""Retrieve data from external APIs."""
from __future__ import annotations

import functools
import json
from enum import Enum

import requests

from metamock.logger import create_logger
from metamock.logger_decorator import error_exception


class EndPoints(Enum):

    """Endpoints we can retrieve data from."""

    MUNICIPALITIES = "https://ws.geonorge.no/kommuneinfo/v1/kommuner"


logger = create_logger(__name__)


@error_exception(logger)
@functools.cache
def get_municipalities() -> list[dict[str, str]]:
    """Get a list of municipalities in Norway."""
    response: requests.Response = requests.get(
        EndPoints.MUNICIPALITIES.value,
        timeout=5,
    )
    return json.loads(response.text)
