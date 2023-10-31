"""General utilities."""
from __future__ import annotations

from metamock.logger import create_logger
from metamock.logger_decorator import error_exception

logger = create_logger(__name__)


@error_exception(logger)
def extract_id_from_uri(uri: str | None, uri_base: str) -> str | None:
    """Extract the ID from a URI.

    Arguments:
    ---------
        uri: The URI to extract the ID from.
        uri_base: The part of the URI prior to the ID.

    Example usage with Klass:
    >>> extract_id_from_uri("https://data.ssb.no/api/klass/v1/classifications/123", "https://data.ssb.no/api/klass/v1/classifications/")
    '123'

    Example usage with VarDok:
    >>> extract_id_from_uri("https://www.ssb.no/a/metadata/conceptvariable/vardok/26/nb", "https://www.ssb.no/a/metadata/conceptvariable/vardok/")
    '26'
    """
    if uri is not None and uri.startswith(
        uri_base,
    ):
        return uri.replace(
            uri_base,
            "",
        ).split(
            "/",
        )[0]
    return None
