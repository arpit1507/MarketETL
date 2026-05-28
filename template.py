import os
from pathlib import Path
import logging

project_name = "MarketETL"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(project_name)
list_of_files = [
    "main.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/entity/config_entity.py",
    f"src/{project_name}/config/__init__.py",
    "config/config.yaml",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/common.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/constants/__init__.py",
    ".github/workflows/marketetl.yml",
    "requirements.txt",
    ".gitignore",
    "setup.py",
    "templates/index.html",
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

