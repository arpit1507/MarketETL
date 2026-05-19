import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

__version__ = "0.0.1"

REPO_NAME="MarketETL"
AUTHOR_USER_NAME="Arpit1507"
AUTHOR_EMAIL="agrawal.arpit03@nmims.edu.in"
SRC_REPO="MarketETL"

setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A small python package for MLflow tutorial",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",

    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },

    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src")
)
