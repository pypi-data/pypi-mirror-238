from setuptools import setup, find_packages
from docsbot.version import APP_VERSION

with open("README.md") as f:
    long_description = f.read()

setup(
    name='docsbot',
    version=APP_VERSION,
    description='A simple chat bot for querying information from your local private documents.',
    url='https://github.com/DataMini/docsbot',
    author='lele',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'docsbot = docsbot.cli:main',
        ]
    },
    install_requires=[
        "chromadb==0.4.5",
        "prettytable",
        "langchain>=0.0.253",
        "qdrant-client",
        "unstructured",
        "pytesseract",
        "openai",
        "python-docx",
        "nltk",
        "tiktoken",
    ]
)


