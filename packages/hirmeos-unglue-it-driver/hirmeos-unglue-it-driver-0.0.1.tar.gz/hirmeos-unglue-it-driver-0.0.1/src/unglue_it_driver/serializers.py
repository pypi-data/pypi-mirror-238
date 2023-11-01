from typing import List

from pydantic import BaseModel, Field


class UnglueReportItem(BaseModel):
    downloads: int = Field(alias="download_count")
    isbn: str
