from pydantic import constr, BaseModel

class Regions(BaseModel):
    region_id: int
    region_name: str