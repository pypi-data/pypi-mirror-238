'''
This file is to aggregate necessary directories
And combine/validate all configuation
'''

from pathlib import Path

from pydantic import BaseModel
from strictyaml import YAML, load

# Project Directories
PACKAGE_ROOT = Path(__file__).resolve().parent.parent
ROOT = PACKAGE_ROOT.parent
YAML_FILE_PATH = PACKAGE_ROOT / "config.yml"
DATASET_DIR = PACKAGE_ROOT / "datasets"
TRAINED_MODEL_DIR = PACKAGE_ROOT / "trained_models"


class AppConfig(BaseModel):
    '''
    High-level application configuation
    '''

    package_name: str
    training_data_file: str
    test_data_file: str
    model_save_file: str


class ModelConfig(BaseModel):
    '''Model-related configuation'''

    target: str
    features: list[str]
    test_size: float
    random_state: int
    penalty: str
    solver: str
    vars_to_check_existance: list[str]
    numerical_vars_with_na: list[str]
    vars_to_log_transform: list[str]
    vars_to_binarize: list[str]


class Config(BaseModel):
    '''Main configuration object'''

    app_config: AppConfig
    model_config: ModelConfig


def find_yaml_file() -> Path:
    '''Locate the configuration file.'''

    if YAML_FILE_PATH.is_file():
        return YAML_FILE_PATH
    raise Exception(f".yml not found at {YAML_FILE_PATH!r}")


def fetch_config_from_yaml(yml_path: Path = None) -> YAML:
    '''Parsing .yml file'''

    if not yml_path:
        yml_path = find_yaml_file()

    if yml_path:
        with open(yml_path, "r") as conf_file:
            parsed_config = load(conf_file.read())
            return parsed_config
    raise OSError(f"Did not find config file at path: {yml_path}")


def create_and_validate_config(parsed_config: YAML = None) -> Config:
    '''Validate all config values from the .yml file'''

    if parsed_config is None:
        parsed_config = fetch_config_from_yaml()

    # specify the data attribute from the strictyaml YAML type.
    _config = Config(app_config = AppConfig(**parsed_config.data), 
                     model_config = ModelConfig(**parsed_config.data),
                     )
    return _config

config = create_and_validate_config()
