import os
import sys
from six.moves import urllib
import zipfile
from crimedetection.logger import logging
from crimedetection.exception import CrimeException
from crimedetection.entity.config_entity import DataIngestionConfig
from crimedetection.entity.artifacts_entity import DataIngestionArtifact


class DataIngestion:
    def __init__(
        self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()
    ):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CrimeException(e, sys)

    def download_data(self) -> str:
        """
        Fetch data from the url
        """

        try:
            dataset_url = self.data_ingestion_config.data_download_url
            zip_download_dir = self.data_ingestion_config.data_ingestion_dir
            os.makedirs(zip_download_dir, exist_ok=True)
            data_file_name = os.path.basename(dataset_url)
            zip_file_path = os.path.join(zip_download_dir, data_file_name)
            logging.info(
                f"Downloading data from {dataset_url} into file {zip_file_path}"
            )
            urllib.request.urlretrieve(dataset_url, zip_file_path)
            logging.info(
                f"Downloaded data from {dataset_url} into file {zip_file_path}"
            )
            return zip_file_path

        except Exception as e:
            raise CrimeException(e, sys)

    def extract_zip_file(self, zip_file_path: str) -> str:
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        try:
            feature_store_path = self.data_ingestion_config.feature_store_file_path
            os.makedirs(feature_store_path, exist_ok=True)

            with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
                # Get a list of all files and directories in the zip
                for file_info in zip_ref.infolist():
                    # Skip _MACOSX and any files starting with '.' (hidden files)
                    if file_info.filename.startswith(
                        "_MACOSX"
                    ) or file_info.filename.startswith("."):
                        continue

                    # Create directories if needed
                    if file_info.is_dir():
                        continue

                    # Extract file if it's not in the _MACOSX folder
                    extracted_path = os.path.join(
                        feature_store_path, file_info.filename
                    )
                    # Create directories in the path if they do not exist
                    if not os.path.exists(os.path.dirname(extracted_path)):
                        os.makedirs(os.path.dirname(extracted_path))

                    with zip_ref.open(file_info) as source, open(
                        extracted_path, "wb"
                    ) as target:
                        target.write(source.read())

            logging.info(
                f"Extracting zip file: {zip_file_path} into dir: {feature_store_path}"
            )

            return feature_store_path

        except Exception as e:
            raise CrimeException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")
        try:
            zip_file_path = self.download_data()
            feature_store_path = self.extract_zip_file(zip_file_path)

            data_ingestion_artifact = DataIngestionArtifact(
                data_zip_file_path=zip_file_path, feature_store_path=feature_store_path
            )

            logging.info(
                "Exited initiate_data_ingestion method of Data_Ingestion class"
            )
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")

            return data_ingestion_artifact

        except Exception as e:
            raise CrimeException(e, sys)
