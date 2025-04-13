from __future__ import annotations
from pydantic import BaseModel


class Countries(BaseModel):
    country_id: str # CHAR(2) primary key
    country_name: str
    region_id: int
