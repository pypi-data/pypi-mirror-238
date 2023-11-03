from setuptools import setup, find_packages
from pathlib import Path

# Get the current directory of the setup.py file (as this is where the README.md will be too)
current_dir = Path(__file__).parent
long_description = (current_dir / "README.md").read_text()

# Set up the package metadata
setup(
    name="psusannx_pipeline",
    author="Jamie O'Brien",
    author_email="jamieob63@gmail.com",
    description="A package containing classes to be used in the preprocessing data pipeline for the PSUSANNX project.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.1.14",
    packages=find_packages(include=["psusannx_pipeline", "psusannx_pipeline.*"]),
    install_requires=[
        "numpy", 
        "pandas", 
        "scikit-learn",
        "category-encoders>=2.2.2"
    ],
    python_requires="==3.*",
    project_urls={
        "Source Code": "https://github.com/jamieob63/psusannx_pipeline.git",
        "Bug Tracker": "https://github.com/jamieob63/psusannx_pipeline.git/issues",
    }
)