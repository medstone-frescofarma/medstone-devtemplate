from datetime import datetime
from typing import List, Optional, ForwardRef, Union

from pydantic import BaseModel, Field, constr

class AuthorizationCreate(BaseModel):
    name        : str
    description : str

class AuthorizationPatch(BaseModel):
    id          : int

    name        : Optional[str] = None
    description : Optional[str] = None

class Authorization(BaseModel):
    id          : int

    name        : str
    description : str

    class Config:
        orm_mode = True

class RoleCreate(BaseModel):
    parent_id       : int
    name            : str
    description     : str
    authorizations  : Optional[List[Union[Authorization, int]]] = None

class UserRole(BaseModel):
    '''Slimmed down version of a normal role: no children included'''
    id          : int
    parent_id   : Optional[int] = None
    name        : str
    description : str

    class Config:
        orm_mode = True

Role = ForwardRef('Role')

class Role(UserRole):
    children        : List[Role]
    authorizations  : List[Authorization]

Role.update_forward_refs()

class RolePatch(BaseModel):
    id              : int
    parent_id       : Optional[int] = None
    name            : Optional[str] = None
    description     : Optional[str] = None
    authorizations  : Optional[List[Union[Authorization, int]]] = None

class UserBase(BaseModel):
    email       : str
    username    : constr(min_length=3, max_length=50)
    name        : Optional[str] = None
    is_admin    : bool
    is_active   : bool
    roles       : Optional[List[Union[UserRole, int]]] = None

class UserCreate(UserBase):
    password    : str

class UserPatch(BaseModel):
    id          : int
    email       : Optional[str] = None
    username    : Optional[str] = None
    name        : Optional[str] = None
    password    : Optional[str] = None
    is_admin    : Optional[bool] = None
    is_active   : Optional[bool] = None
    reset_2fa   : Optional[bool] = False
    roles       : Optional[List[Union[UserRole, int]]] = None

class User(UserBase):
    id          : int
    created_at  : datetime
    updated_at  : datetime
    last_login  : Optional[datetime] = None
    has_2fa     : Optional[bool] = False
    is_2fa_authenticated : Optional[bool] = False

    class Config:
        orm_mode = True
