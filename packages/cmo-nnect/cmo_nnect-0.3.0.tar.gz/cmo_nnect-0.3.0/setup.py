from setuptools import setup, find_packages
from pathlib import Path

# read the contents of the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="cmo_nnect",
    version="0.3.0",
    python_requires=">=3.8",
    description="Connect with a variety of API's with ease.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Thijs van der Velden, Koen Leijsten",
    author_email="service@cmotions.nl",
    keyword=[
        "API",
        "Connector",
        "Connectors",
        "Dynamics",
        "AFAS Profit",
        "Profit",
        "Nmbrs",
        "Mautic",
        "Exact",
        "Finance and Operations",
        "Freshsales",
        "Freshdesk",
        "Exact",
        "Notion",
        "Piano",
        "Recruitee",
        "KNMI",
        "Braze",
        "Salesforce",
        "Salesforce Marketing Cloud",
        "Kadaster",
        "Google Analytics",
        "Google Analytics 4",
        "Business Central",
    ],
    url="https://dev.azure.com/Cmotions/Packages/_git/cmo_nnect",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "requests",
        "zeep",
        "flatten_json",
        "tqdm",
        "msal",
        "google-analytics-data",
        "google-oauth2-tool",
        "azure-identity",
        "azure-keyvault",
    ],
    extras_require={
        "dev": [
            "black",
            "jupyterlab",
            "pytest>=6.2.4",
            "python-dotenv",
            "ipykernel",
            "twine",
        ],
    },
)
