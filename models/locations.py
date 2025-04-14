from typing import Optional

from pydantic import constr, BaseModel


class Locations(BaseModel):
    location_id: int
    street_address: str
    postal_code: str
    city: str
    state_province: str
    country_id: constr(min_length=2, max_length=2)