import os, sys
import shutil
from crimedetection.logger import logging
from crimedetection.exception import CrimeException
from crimedetection.entity.config_entity import DataValidationConfig
from crimedetection.entity.artifacts_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
)


class DataValidation:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig,
    ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config

        except Exception as e:
            raise CrimeException(e, sys)

    def validate_all_files_exist(self) -> bool:
        try:
            validation_status = True

            all_files = os.listdir(self.data_ingestion_artifact.feature_store_path)

            # Filter out hidden files and folders
            visible_files = [
                file
                for file in all_files
                if not file.startswith(".") and file != "__MACOSX"
            ]

            required_files = set(self.data_validation_config.required_file_list)
            present_files = set(visible_files)

            # Check if all required files are present
            missing_files = required_files - present_files

            if missing_files:
                validation_status = False

            # Write validation status to file
            os.makedirs(self.data_validation_config.data_validation_dir, exist_ok=True)
            with open(self.data_validation_config.valid_status_file_dir, "w") as f:
                f.write(f"Validation status: {validation_status}")

            return validation_status

        except Exception as e:
            raise SignException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        logging.info("Entered initiate_data_validation method of DataValidation class")
        try:
            status = self.validate_all_files_exist()
            data_validation_artifact = DataValidationArtifact(validation_status=status)

            logging.info(
                "Exited initiate_data_validation method of DataValidation class"
            )
            logging.info(f"Data validation artifact: {data_validation_artifact}")

            if status:
                shutil.copy(
                    self.data_ingestion_artifact.data_zip_file_path, os.getcwd()
                )

            return data_validation_artifact

        except Exception as e:
            raise CrimeException(e, sys)
