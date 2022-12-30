from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel


class CreatePOIRequest(BaseModel):
    name: str
    dob: datetime
    profession: Optional[str]
    risk_factor: Literal["NA", "Low", "Medium", "High", "Extreme"]


class PersonOfInterest(CreatePOIRequest):
    poi_id: str
    date_received: datetime


class CreateResponse(BaseModel):
    status: Optional[str] = "successful"
    id: str
