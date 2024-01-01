from importlib.metadata import metadata
from typing import Optional

from pydantic import field_validator, AnyUrl, BaseModel, EmailStr, Field

from ancv import PACKAGE


class Metadata(BaseModel):
    """Modeling Python package metadata.

    Modelled after the Python core metadata specification:
    https://packaging.python.org/en/latest/specifications/core-metadata/ .
    Not all fields were implemented for lack of ability of testing.

    For more context, see:

        - https://docs.python.org/3/library/importlib.metadata.html#metadata
        - https://peps.python.org/pep-0566/
    """

    metadata_version: str = Field(
        description="Version of the metadata format, e.g. '2.1'",
    )
    name: str = Field(
        description="Name of the package, e.g. 'ancv'",
        pattern=r"(?i)^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$",
    )
    version: str = Field(
        description="Version of the package, e.g. '0.1.0'",
        # https://peps.python.org/pep-0440/#appendix-b-parsing-version-strings-with-regular-expressions
        pattern=r"^([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?$",
    )
    summary: Optional[str] = Field(
        None, description="One-line summary of the package, e.g. 'Ancv is a package for ...'",
    )
    home_page: Optional[AnyUrl] = Field(
        None, description="Homepage of the package, e.g. https://ancv.io/'"
    )
    download_url: Optional[AnyUrl] = Field(
        None, description="URL to download this version of the package"
    )
    license: Optional[str] = Field(None, description="License of the package, e.g. 'MIT'")
    author: Optional[str] = Field(None, description="Author of the package, e.g. 'John Doe'")
    author_email: Optional[EmailStr] = Field(
        None, description="Email of the author, e.g. john@doe.com'"
    )
    requires_python: Optional[str] = Field(
        None, description="Python version required by the package, e.g. '>=3.6'",
    )
    classifier: Optional[list[str]] = Field(
        None, description="Classifiers of the package, e.g. 'Programming Language :: Python :: 3.6'",
    )
    requires_dist: Optional[list[str]] = Field(
        None, description="Distributions required by the package, e.g. 'aiohttp[speedups] (>=3.8.1,<4.0.0)'",
    )
    project_url: Optional[list[str]] = Field(
        None, description="Project URLs of the package, e.g. 'Repository, https://github.com/namespace/ancv/'",
    )
    description_content_type: Optional[str] = Field(
        None, description="Content type of the description, e.g. 'text/plain'",
    )
    description: Optional[str] = Field(
        None, description="Long description of the package, e.g. 'Ancv is a package for ...'",
    )

    @field_validator("project_url")
    @classmethod
    def strip_prefix(cls, v: Optional[list[str]]) -> Optional[list[str]]:
        """Strips the prefixes 'Name, ' from the URLs.

        For example, extracts just the URL from:
        'Repository, https://github.com/namespace/ancv/'.
        """
        if v is None:
            return v
        return [url.split()[-1] for url in v]


METADATA = Metadata.parse_obj(metadata(PACKAGE).json)
