import setuptools
from setuptools import find_packages

import os

# Get the absolute path of the directory containing setup.py
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to requirements.txt in the parent directory
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
requirements_path = "C:/Users/sophi/OneDrive/Documents/Data Science/guardrail/requirements.txt"

requirements = []
try:
    with open(requirements_path) as f:
        requirements = f.read().splitlines()
except FileNotFoundError:
    print(f"Error: 'requirements.txt' file not found at {requirements_path}.")
except Exception as e:
    print(f"An error occurred while reading 'requirements.txt': {e}")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="guardrail-ml",
    version="0.0.16",
    packages=find_packages(exclude=["tests", "guardrailmlenv", "examples", "docs", "env", "dist"]),
    package_data={'guardrail': ['firewall/output_detectors/factuality_detector/prompts/*.yaml', 'firewall/patterns/*.json']},
    author="Kevin Wu",
    author_email="kevin@guardrailml.com",
    description="Monitor LLMs with custom metrics to scale with confidence",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.guardrailml.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "textstat",
        "transformers<=4.30.2",
        "sentencepiece",
        "sentence-transformers",
        "accelerate",
        "bitsandbytes",
        "cleantext",
        "unidecode",
        "pillow",
        "jsonformer",
        "scipy",
        "pydantic<=2.0.3",  # Specifying the version
        "tenacity",
        "colorama",
        "openai",
        "python-dotenv",
        "einops",
        "langchain",
        "Faker",
        "tensorflow",  # Specifying the version
        "presidio-analyzer<=2.2.33",  # Specifying the version
        "presidio-anonymizer<=2.2.33",  # Specifying the version
        "genbit",  # Specifying the version
        "jsonlines",
        "pydantic-settings<=2.0.3",  # Specifying the version
        "detect-secrets",
        "tiktoken",
        "spacy-transformers",
        "fasttext"
        "fasttext-langdetect"

    ],
)
