from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from medstone_backend.db.deps import get_db
from medstone_backend.serializers import common_serializer, auth_serializer, user_serializer
from medstone_backend.services import auth_service

# from app import crud, models, schemas
# from medstone_backend.api import deps
# from medstone_backend.core import security
# from medstone_backend.core.config import settings
# from medstone_backend.core.security import get_password_hash
# from medstone_backend.utils import (
#     generate_password_reset_token,
#     send_reset_password_email,
#     verify_password_reset_token,
# )

router = APIRouter()


@router.post("/login/access-token", response_model=auth_serializer.Token)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    login_request = auth_serializer.UserLoginRequest(
        username=form_data.username,
        password=form_data.password
    )
    return auth_service.authenticate_user(db, login_request)

@router.post("/login", response_model=auth_serializer.Token)
def login_access_token(
    login_request: auth_serializer.UserLoginRequest, db: Session = Depends(get_db)
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    return auth_service.authenticate_user(db, login_request)

@router.post("/login/test-token", response_model=user_serializer.User)
def test_token(current_user: user_serializer.User = Depends(auth_service.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery/{email}", response_model=common_serializer.Msg)
def recover_password(email: str, db: Session = Depends(get_db)) -> Any:
    """
    Password Recovery
    """
    user = crud.user.get_by_email(db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    return {"msg": "Password recovery email sent"}


@router.post("/reset-password/", response_model=common_serializer.Msg)
def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(get_db),
) -> Any:
    """
    Reset password
    """
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()
    return {"msg": "Password updated successfully"}
