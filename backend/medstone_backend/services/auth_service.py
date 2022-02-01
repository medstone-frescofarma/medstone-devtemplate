from datetime import datetime, timedelta

import jwt
import pyotp
from pydantic import ValidationError
from sqlalchemy.orm import Session

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from medstone_backend.config import config
from medstone_backend.db.deps import get_db
from medstone_backend.services import user_service
from medstone_backend.models import user_models
from medstone_backend.serializers import auth_serializer

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login/access-token"
)

def authenticate_user(db: Session, login_request : auth_serializer.UserLoginRequest) -> auth_serializer.Token:
    '''Small function to check if username & password match, and generate JWT token if yes'''
    # check if a user with this username exists
    user_1 = user_service.get_user_by_email(db, login_request.username)
    user_2 = user_service.get_user_by_username(db, login_request.username)
    if user_1 or user_2:
        # select one of the two users, default to user by email
        user = user_1 if user_1 else user_2
        password_ok = user.check_password(login_request.password)
        if password_ok:
            # green light for login, set last login date/time to now
            user.last_login = datetime.now()
            db.add(user)
            db.commit()
            # generate the time when this token will expire
            expiration_date = datetime.utcnow() + timedelta(hours=3)
            # generate the token payload data we'll sign
            token_payload = auth_serializer.TokenPayload()
            token_payload.sub = user.id
            token_payload.exp = expiration_date
            token_payload.tfa = False
            # do the signing process using our secret key
            token_data = jwt.encode(dict(token_payload), config.JWT_SECRET_KEY, algorithm='HS256')
            # generate the token we'll send back to the client
            token = auth_serializer.Token(
                access_token=token_data,
                token_type='Bearer'
            )
            return token
    raise HTTPException(
        status_code=400, detail="Incorrect username or password"
    )


def get_current_user(
        db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
    ) -> user_models.User:
    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=['HS256'])
        token_data = auth_serializer.TokenPayload(**payload)
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    # load the user from the database
    user = user_service.get_user(db, user_id=token_data.sub)
    # set the two-factor status on the user
    user.is_2fa_authenticated = token_data.tfa
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_active_user(
    current_user: user_models.User = Depends(get_current_user),
) -> user_models.User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_current_active_superuser(
    current_user: user_models.User = Depends(get_current_user),
) -> user_models.User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user

def generate_tfa_qr_data(
        db : Session,
        current_active_user : user_models.User,
    ) -> str:
    # check if the user already had a totp secret
    if current_active_user.totp_secret == None:
        # generate the user's secret and save it immediately
        current_active_user.totp_secret = pyotp.random_base32()
        db.add(current_active_user)
        db.commit()
        qr_code_data = pyotp.totp.TOTP(current_active_user.totp_secret).provisioning_uri(
            name=current_active_user.username,
            issuer_name='Farmadam Voorraad Portaal'
        )
        return qr_code_data
    else:
        raise HTTPException(status_code=400, detail='User already has TOTP secret')

def authenticate_user_tfa(
        current_active_user : user_models.User,
        otp : str
    ):
    if current_active_user.totp_secret:
        totp = pyotp.TOTP(current_active_user.totp_secret)
        if totp.verify(otp, valid_window=1):
            # generate the time when this token will expire
            expiration_date = datetime.utcnow() + timedelta(minutes=30)
            # generate the token payload data we'll sign
            token_payload = auth_serializer.TokenPayload()
            token_payload.sub = current_active_user.id
            token_payload.exp = expiration_date
            token_payload.tfa = True
            # do the signing process using our secret key
            token_data = jwt.encode(dict(token_payload), config.JWT_SECRET_KEY, algorithm='HS256')
            # generate the token we'll send back to the client
            token = auth_serializer.Token(
                access_token=token_data,
                token_type='Bearer'
            )
            return token
        else:
            raise HTTPException(status_code=400, detail='Incorrect TOTP')
    else:
        raise HTTPException(status_code=400, detail='No TOPT secret set')
