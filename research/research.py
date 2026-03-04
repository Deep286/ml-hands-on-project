from dataclasses import dataclass
from pathlib import Path
from src.ml_hands_on_project.constants import *
from src.ml_hands_on_project.utils.common import read_yaml, create_directories
from src.ml_hands_on_project import logger
import os
import zipfile
from urllib.request import urlretrieve


@dataclass
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path

class ConfigurationManager:
    def __init__(self, 
            config_filepath=CONFIG_FILE_PATH,   # pyright: ignore[reportUndefinedVariable]
            params_filepath=PARAMS_FILE_PATH,   # pyright: ignore[reportUndefinedVariable]
            schema_filepath=SCHEMA_FILE_PATH):  # pyright: ignore[reportUndefinedVariable]
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)

        create_directories([self.config.artifact_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir
        )
        return data_ingestion_config

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
    
    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            filename, headers = urlretrieve(self.config.source_URL, self.config.local_data_file)
            logger.info(f"Downloaded file and saved to {filename}")
        else:
            logger.info(f"File already exists at {self.config.local_data_file}")
    
    def extract_zip_file(self):
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)  
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
        logger.info(f"Extracted file and saved to {unzip_path}")
    

try:
    config = ConfigurationManager()
    data_ingestion_config = config.get_data_ingestion_config()
    data_ingestion = DataIngestion(config=data_ingestion_config)
    data_ingestion.download_file()
    data_ingestion.extract_zip_file()
except Exception as e:
    logger.exception(e)
    raise e