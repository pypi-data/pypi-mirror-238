"""Get and generate synthetic data from a variety of sources."""
from __future__ import annotations

import random
import typing
from typing import TYPE_CHECKING

from datadoc_model import Enums
from faker import Faker

from metamock.logger import create_logger
from metamock.logger_decorator import error_exception

if TYPE_CHECKING:
    from datetime import date

from metamock.snr_manager import SnrFnrManager

faker = Faker("no_NO")
snr_fnr_manager = SnrFnrManager()


def is_fnr(short_name: str) -> bool:
    """Return True if this column is a Norwegian personal number."""
    short_name = short_name.lower().strip().replace("_", "")
    return "fnr" in short_name


def is_snr(short_name: str) -> bool:
    """Return True if this column is a snr Number."""
    short_name = short_name.lower().strip().replace("_", "")
    return "snr" in short_name


logger = create_logger(__name__)


@error_exception(logger)
def is_ssid(short_name: str) -> bool:
    """Return True if this column is a Norwegian Personal Number."""
    short_name = short_name.lower().strip().replace("_", "")
    return "fnr" in short_name or "snr" in short_name


FUNCTION_COLUMN_NAME_MAPPING = {
    faker.name: ["navn"],
    faker.iana_id: ["kod"],
    faker.city: ["skolenavn", "sted", "by"],
    faker.date: ["dato", "start", "avsl"],
}


@error_exception(logger)
def get_string(
    column_name: str,
    mapping: dict[typing.Callable[[], str], list[str]] = FUNCTION_COLUMN_NAME_MAPPING,
) -> str:
    """Generate synthetic string data."""
    column_name = column_name.lower()

    if is_fnr(column_name):
        return snr_fnr_manager.get_fnr()

    if is_snr(column_name):
        return snr_fnr_manager.get_snr()

    for function, name_parts in mapping.items():
        if any(bool(part in column_name.lower().strip()) for part in name_parts):
            return function()

    return faker.word()


@error_exception(logger)
def get_datetime() -> date:
    """Generate synthetic date data."""
    return faker.date_object()


@error_exception(logger)
def get_integer(
    column_name: str,
    row_number: int,
    *,
    identifier: bool = False,
) -> int:
    """Generate synthetic integer data."""
    column_name = column_name.lower()

    match column_name:
        case "alder":
            return faker.random_int(min=0, max=110)

        case "hkltrinn":
            return faker.random_int(min=1, max=13)

    if identifier is True:
        return faker.unique.random_int(min=0, max=row_number * 2)

    return random.randint(0, 1000)  # noqa:S311 non-cryptographic


@error_exception(logger)
def generate_data_for_data_type(
    data_type: Enums.Datatype,
    column_name: str,
    length: int,
    *,
    identifier: bool = False,
) -> list[typing.Any] | None:
    """Generate synthetic data for the given data type."""

    def generate_string(column_name: str = column_name) -> str:
        """Pipe arguments to the get_string function."""
        return get_string(column_name)

    def generate_integer(
        column_name: str = column_name,
        length: int = length,
        *,
        identifier: bool = identifier,
    ) -> int:
        """Pipe the arguments to the get_integer function."""
        return get_integer(column_name, length, identifier=identifier)

    functions: dict[Enums.Datatype, typing.Callable[[], typing.Any]] = {
        Enums.Datatype.STRING: generate_string,
        Enums.Datatype.INTEGER: generate_integer,
        Enums.Datatype.DATETIME: lambda: get_datetime(),
        Enums.Datatype.BOOLEAN: lambda: random.choice(  # noqa: S311 non-cryptographic
            [True, False],
        ),
        Enums.Datatype.FLOAT: lambda: random.uniform(  # noqa: S311 non-cryptographic
            0,
            1000,
        ),
    }
    try:
        return [functions[data_type]() for _ in range(length)]
    except KeyError:
        return None
