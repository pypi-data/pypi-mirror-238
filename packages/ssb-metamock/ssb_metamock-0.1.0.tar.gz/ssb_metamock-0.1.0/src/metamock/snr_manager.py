"""Get data from the shared catalogue."""

import secrets

import pandas as pd
import pyarrow.parquet as pq
from dapla import AuthClient, gcs

from metamock.logger import create_logger
from metamock.logger_decorator import error_exception

PATH: str = "ssb-prod-demo-stat-b-data-delt/snr-kat-latest-parquet/*.parquet"
logger = create_logger(__name__)


class SnrFnrManager:

    """Manages the connection to the shared cataloge, and retrieving snr/fnr."""

    snr_list: list = []  # noqa: RUF012
    fnr_list: list = []  # noqa: RUF012

    @error_exception(logger)
    def read_df_from_bucket(self) -> pd.DataFrame:
        """Read files from bucket and create a pandas containing snr/fnr."""
        gc_file_system = gcs.GCSFileSystem(token=AuthClient.fetch_google_credentials())
        files_in_bucket = gc_file_system.glob(PATH)

        snr_fnr_df: pd.DataFrame = (
            pq.ParquetDataset(files_in_bucket, filesystem=gc_file_system)
            .read()
            .to_pandas()[["fnr", "snr"]]
        )

        return snr_fnr_df

    @error_exception(logger)
    def get_snr_fnr_from_shared_catalogue(self) -> None:
        """Retrieve content of the shared catalogue, and returns a DataFrame with fnr and snr columns."""
        snr_fnr_df: pd.DataFrame = self.read_df_from_bucket()

        self.snr_list = snr_fnr_df["snr"].to_list()
        self.fnr_list = snr_fnr_df["fnr"].to_list()

    @error_exception(logger)
    def get_snr(self) -> str:
        """Get a random snr number."""
        if len(self.snr_list) == 0:
            self.get_snr_fnr_from_shared_catalogue()

        return secrets.choice(self.snr_list)

    @error_exception(logger)
    def get_fnr(self) -> str:
        """Get a random fnr number."""
        if len(self.fnr_list) == 0:
            self.get_snr_fnr_from_shared_catalogue()

        return secrets.choice(self.fnr_list)
