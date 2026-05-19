import os
from pathlib import Path
import logging

project_name = "MarketETL"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(project_name)
list_of_files = [
    "main.py",
    "src/entity/__init__.py",
    "src/entity/config_entity.py",
    "src/config/__init__.py",
    "config/config.yaml",
    "src/utils/__init__.py",
    "src/utils/common.py",
    "src/components/__init__.py",
    "src/pipeline/__init__.py",
    "requirements.txt",
    ".gitignore",
    "setup.py",
    "template/index.html",
    "README.md",
    "params.yaml"
]

for file in list_of_files:
    Path(file).parent.mkdir(parents=True, exist_ok=True)
    if not os.path.exists(file):
        with open(file, "w") as f:
            pass
        logger.info(f"Created file: {file}")
    else:
        logger.info(f"File already exists: {file}")

