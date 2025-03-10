from pydantic import BaseModel

class ApiRequest(BaseModel):
    coordinates: list
    start_date: str
    end_date: str
    vh_threshold: float = 1.25
    ndwi_threshold: float = 0
    mndwi_threshold: float = 0
