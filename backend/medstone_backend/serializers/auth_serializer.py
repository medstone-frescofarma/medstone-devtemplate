from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class UserLoginRequest(BaseModel):
    username    : str
    password    : str

class UserLoginSuccessResponse(BaseModel):
    token       : str

class UserLoginFailedResponse(BaseModel):
    message     : str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None
    exp: Optional[datetime] = None
    tfa: Optional[bool] = None
