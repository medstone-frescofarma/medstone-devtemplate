from typing import List

from pydantic import BaseModel

from medstone_backend.serializers import user_serializer, location_serializer


class Msg(BaseModel):
    msg: str

class CommonResponse(BaseModel):
    user: user_serializer.User
    locations: List[location_serializer.Location]
