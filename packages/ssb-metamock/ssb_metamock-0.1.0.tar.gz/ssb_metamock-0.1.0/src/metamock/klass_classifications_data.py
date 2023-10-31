"""Functionality relating to Klass."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING

from klass.classes.classification import KlassClassification

from metamock.logger import create_logger
from metamock.logger_decorator import error_exception
from metamock.utils import extract_id_from_uri

if TYPE_CHECKING:
    import pandas as pd

# Keep this dict in numeric order
CLASSIFICATION_COLUMN_NAME_MAPPING: dict[str, list[str]] = {
    "1": ["fskolenr"],
    "2": ["kjonn", "kjoenn"],
    "6": ["nace", "naering"],
    "31": ["mrk_dl"],
    "36": ["nus2000", "emnekode", "vidutd", "utdkode"],
    "66": ["fakultet"],
    "91": ["stat", "borg"],
    "100": ["land"],
    "127": ["fylk"],
    "131": ["skolekom", "komm"],
}

KLASS_URI_BASE: str = "https://www.ssb.no/klass/klassifikasjoner/"

logger = create_logger(__name__)


@error_exception(logger)
def get_codes_for_klass_classification(classification_id: str) -> pd.Series:
    """Get codes for a given Classification ID."""
    return KlassClassification(classification_id).get_codes().data["code"]


@error_exception(logger)
def generate_data_from_klass_codes(
    column_name: str | None,
    classification_uri: str,
    length: int,
) -> list | None:
    """Generate a column of synthetic data based on the code list from a classification.

    If there is a defined URI in the metadata, use that.
    If we can guess a classification based on the name of the column, use that.
    If we can't find a matching classification, just return None.
    """
    classification_id = extract_id_from_uri(
        classification_uri,
        KLASS_URI_BASE,
    )
    if not classification_id:
        classification_id = guess_classification_from_name(
            column_name,
        )

    if not classification_id:
        # We didn't find a matching classification so stop here
        return None

    return [
        random.choice(  # noqa:S311 non-cryptographic
            get_codes_for_klass_classification(
                classification_id,  # type: ignore [arg-type]
            ),
        )
        for _ in range(length)
    ]


@error_exception(logger)
def is_code(column_name: str | None) -> bool:
    """Return true if we should use the classification code, otherwise we use the value."""
    if not column_name:
        return False
    return "kode" in column_name or "nr" in column_name


@error_exception(logger)
def guess_classification_from_name(
    column_name: str | None,
    mapping: dict[str, list[str]] = CLASSIFICATION_COLUMN_NAME_MAPPING,
) -> str | None:
    """Get a classification ID if we know of one."""
    if not column_name:
        return None
    for classification_id, name_parts in mapping.items():
        if any(bool(part in column_name.lower().strip()) for part in name_parts):
            return classification_id
    return None
