"""Generate synthetic data from a Datadoc document."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from enum import Enum
from pprint import pprint

import numpy as np
import pandas as pd
from dapla import FileClient
from datadoc_model import Enums
from datadoc_model.Model import DataDocVariable

from metamock.faker_data import generate_data_for_data_type
from metamock.klass_classifications_data import generate_data_from_klass_codes
from metamock.logger import create_logger
from metamock.logger_decorator import error_exception
from metamock.vardok_data import generate_data_from_vardok

DEFAULT_NUMBER_OF_ROWS = 10
MAX_ROWS = 1_000_000


class FileType(Enum):

    """Supported file types."""

    CSV = "csv"
    PARQUET = "parquet"
    JSON = "json"


logger = create_logger(__name__)


@error_exception(logger)
def read_metadata_from_file(path_str: str) -> list[DataDocVariable]:
    """Open a file and read metadata into datadoc models."""
    fresh_metadata = {}

    if path_str.startswith("gs://"):
        fresh_metadata = json.load(FileClient.gcs_open(path_str))

    else:
        path: pathlib.Path = pathlib.Path(path_str)

        with path.open(mode="r", encoding="utf-8") as file:
            fresh_metadata = json.load(file)

    variables_list = fresh_metadata.pop("variables", None)

    return [DataDocVariable(**v) for v in variables_list]


@error_exception(logger)
def generate_synthetic_data(
    variable_metadata: list[DataDocVariable],
    rows: int,
) -> pd.DataFrame:
    """Generate synthetic data from the given list of DataDocVariable."""
    # Fill the generated data with NaN as a starting point
    generated_data: pd.DataFrame = pd.DataFrame(
        np.empty((rows, len(variable_metadata))) * np.nan,
        columns=[v.short_name for v in variable_metadata],
    )

    for v in variable_metadata:
        data_list = None
        identifier: bool = v.variable_role == Enums.VariableRole.IDENTIFIER

        if v.classification_uri:
            # First, attempt to get data from Klass since this is the most relevant for SSB.
            data_list = generate_data_from_klass_codes(
                v.short_name,
                v.classification_uri,
                rows,
            )

            klass_info: str = f"{v.short_name}: Generated data from Klass."
            logger.info(klass_info)

        if v.definition_uri and not data_list:
            # Next, see if there's anything relevant in VarDok https://www.ssb.no/a/metadata/definisjoner/variabler/main.html
            data_list = generate_data_from_vardok(v.definition_uri, rows)

            vardok_info: str = f"{v.short_name}: Generated data from vardok."
            logger.info(vardok_info)

        # We couldn't find anything in Klass, so we fall back to generating from the data type
        if v.data_type and not data_list:
            data_list = generate_data_for_data_type(
                Enums.Datatype(v.data_type),
                v.short_name,
                rows,
                identifier=identifier,
            )

            generated_info = f"{v.short_name}: Generated data from data type."
            logger.info(generated_info)

        if data_list:
            generated_data[v.short_name] = data_list

    return generated_data


@error_exception(logger)
def save_data_to_file(
    data: pd.DataFrame,
    folder_path: pathlib.Path,
    file_name: str,
    file_type: FileType,
) -> None:
    """Save the given dataframe to the specified file path."""
    file_name = (
        file_name.replace(FileType.CSV.value, "")
        .replace(FileType.JSON.value, "")
        .replace(FileType.PARQUET.value, "")
    )
    output_path = folder_path / f"{file_name}.{file_type.value.lower()}"
    match file_type:
        case FileType.CSV:
            data.to_csv(
                output_path,
                sep=";",
                encoding="utf-8",
            )

        case FileType.PARQUET:
            data.to_parquet(output_path)

        case FileType.JSON:
            data.to_json(output_path)

    success_message: str = f"Successfully generated synthetic data: {output_path}"
    print(success_message)  # noqa: T201
    logger.info(success_message)


@error_exception(logger)
def main(sys_args: list[str] = sys.argv[1:]) -> None:
    """Run the app."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--datadoc-document",
        type=str,
        help="Metamock is able to read input data from a local file or from Google Cloud Storage. Type the entire path (including 'gs://') to fetch data from a bucket.",
    )
    parser.add_argument("-f", "--output-path", type=pathlib.Path)
    parser.add_argument("-n", "--output-filename", type=str)
    parser.add_argument(
        "-t",
        "--file-type",
        type=str,
        default="parquet",
        choices=[v.value for v in FileType],
    )
    parser.add_argument("-r", "--no-of-rows", type=int, default=DEFAULT_NUMBER_OF_ROWS)
    args = parser.parse_args(sys_args)
    file_type = FileType(args.file_type)

    if args.no_of_rows < 1 or args.no_of_rows > MAX_ROWS:
        parser.error(f"Number of rows must be between 1 and {MAX_ROWS}")

    variable_metadata: list = []

    variable_metadata = read_metadata_from_file(args.datadoc_document)

    if insufficient_metadata := [
        v.short_name for v in variable_metadata if not all([v.data_type, v.short_name])
    ]:
        print(  # noqa: T201
            "WARNING: The following columns contain insufficient metadata and will have empty values in the output dataset.",
        )
        pprint(  # noqa: T203
            insufficient_metadata,
        )

    generated_data: pd.DataFrame = generate_synthetic_data(
        variable_metadata,
        args.no_of_rows,
    )

    save_data_to_file(
        generated_data,
        args.output_path,
        args.output_filename,
        file_type,
    )


if __name__ == "__main__":
    main()
