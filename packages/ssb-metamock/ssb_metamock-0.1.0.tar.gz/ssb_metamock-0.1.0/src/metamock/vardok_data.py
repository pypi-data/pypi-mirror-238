"""Generate data based on a variable from Statistics Norway's variable definition system VarDok."""
from __future__ import annotations

import functools
from typing import TYPE_CHECKING

import defusedxml.ElementTree as et  # noqa: N813
import requests

from metamock.custom_data_generation import generate_organisation_number
from metamock.faker_data import faker
from metamock.klass_classifications_data import (
    KLASS_URI_BASE,
    generate_data_from_klass_codes,
)
from metamock.logger import create_logger
from metamock.logger_decorator import error_exception
from metamock.utils import extract_id_from_uri

if TYPE_CHECKING:
    from xml.etree.ElementTree import Element

VARDOK_URI_BASE = "https://www.ssb.no/a/metadata/conceptvariable/vardok/"
VARDOK_XML_URI_BASE = "https://www.ssb.no/a/xml/metadata/conceptvariable/vardok/"

XML_NAMESPACES = {
    "fimd": "http://www.ssb.no/ns/fimd",
    "xlink": "http://www.w3.org/1999/xlink",
}

VARDOK_ID_FUNCTION_MAPPING = {
    "26": faker.unique.ssn,
    "1350": functools.partial(generate_organisation_number, faker),
}

logger = create_logger(__name__)


@error_exception(logger)
def get_variable_definition(vardok_id: str) -> Element | None:
    """Retrieve the XML definition of a variable from the Vardok API.

    Args:
    ----
        vardok_id (str): The ID of the variable to retrieve.

    Returns:
    -------
        An Element object representing the XML definition of the variable,
        or None if the variable was not found.

    Raises:
    ------
        requests.exceptions.HTTPError: If the API returns an error status code.
        requests.exceptions.Timeout: If the request times out.
    """
    response = requests.get(
        f"{VARDOK_XML_URI_BASE}{vardok_id}/nb",
        timeout=5,
    )
    if response.status_code == requests.codes.internal_server_error:
        # Vardok returns 500 if the variable is not found
        return None
    response.raise_for_status()
    return et.fromstring(response.text)


@error_exception(logger)
def get_referenced_classification_uri(vardok_id: str) -> str | None:
    """Get the URI of the classification referenced by the given variable definition ID.

    Args:
    ----
        vardok_id (str): The ID of the variable definition.

    Returns:
    -------
        str | None: The URI of the referenced classification, or None if not found.
    """
    variable_definition = get_variable_definition(vardok_id)
    try:
        uri = str(
            variable_definition.find("fimd:Relations", XML_NAMESPACES)  # type: ignore [union-attr]
            .find(
                "fimd:ClassificationRelation",
                XML_NAMESPACES,
            )
            .get(f"{{{XML_NAMESPACES['xlink']}}}href"),
        )
        return uri.replace("http://www.ssb.no/classification/klass/", KLASS_URI_BASE)
    except AttributeError:
        return None


@error_exception(logger)
def generate_data_from_vardok(
    definition_uri: str,
    length: int,
) -> list | None:
    """Generate data based on a variable from Statistics Norway's variable definition system VarDok.

    Args:
    ----
        definition_uri (str): The URI of the variable definition in VarDok.
        length (int): The number of data points to generate.

    Returns:
    -------
        list | None: A list of generated data points, or None if the variable is not pre-defined.

    Notes:
    -----
        We can only do something sensible with pre-defined variables, otherwise we just return None.
    """
    vardok_id = extract_id_from_uri(
        definition_uri,
        VARDOK_URI_BASE,
    )

    if not vardok_id:
        return None

    # If there's a linked classification, we can use that to generate data
    if classification_uri := get_referenced_classification_uri(vardok_id):
        return generate_data_from_klass_codes(
            None,
            classification_uri,
            length,
        )

    # Otherwise, we can fall back to known variables
    if function := VARDOK_ID_FUNCTION_MAPPING.get(vardok_id, None):
        return [function() for _ in range(length)]

    return None
