from typing import List, ForwardRef, Optional

from pydantic import BaseModel

Location = ForwardRef('Location')

class Location(BaseModel):
    id          : int
    name        : str
    children    : List[Location]

    class Config:
        orm_mode = True

Location.update_forward_refs()
