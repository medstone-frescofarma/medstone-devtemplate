from typing import Optional

from pydantic import BaseModel

class Address(BaseModel):
    id              : int
    street_name     : Optional[str] = None
    street_number   : Optional[str] = None
    city            : Optional[str] = None
    zipcode         : Optional[str] = None
    country         : Optional[str] = None

    class Config:
        orm_mode = True
