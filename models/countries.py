from __future__ import annotations
from pydantic import BaseModel, constr


class Countries(BaseModel):
    country_id: constr(min_length=2, max_length=2) # CHAR(2) primary key
    country_name: str
    region_id: int
