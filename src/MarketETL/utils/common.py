import os
from box.exceptions import BoxValueError
import yaml
from MarketETL import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any


@ensure_annotations
def read_yaml(path_to_file: Path) -> ConfigBox:
    try:
        with open(path_to_file) as yaml_file:
            content = yaml.safe_load(yaml_file)
            print(content)
            logger.info(f"yaml file: {path_to_file} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError(f"yaml file: {path_to_file} is empty")
    except Exception as e:
        raise e
    
@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}") 
    

@ensure_annotations
def save_json(path: Path, data: dict):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"json file: {path} saved successfully")

@ensure_annotations
def load_bin(path: Path) -> Any:
    data= joblib.load(path)
    logger.info(f"json file: {path} loaded successfully")
    return data
