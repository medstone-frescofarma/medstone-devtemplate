from typing import List

from sqlalchemy.orm import Session, joinedload

from medstone_backend.serializers import user_serializer
from medstone_backend.models import user_models


def get_user(db: Session, user_id: int):
    return db.query(user_models.User).filter(
        user_models.User.id == user_id,
        user_models.User.is_active == True
    ).first()

def get_user_by_id(db : Session, id : int):
    return db.query(user_models.User).filter(user_models.User.id == id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(user_models.User).filter(
        user_models.User.username == username,
        user_models.User.is_active == True
    ).first()

def get_user_by_email(db: Session, email: str):
    return db.query(user_models.User).filter(
        user_models.User.email == email,
        user_models.User.is_active == True
    ).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(user_models.User).offset(skip).limit(limit).all()

def get_role_by_id(db : Session, id : int):
    return db.query(user_models.Role).filter(user_models.Role.id == id).first()

def get_all_roles(db : Session) -> List[user_models.Role]:
    user_models.Role.children.property.strategy.join_depth = 20
    roles = db.query(user_models.Role).filter_by(parent_id=None).options(joinedload('_authorizations')).all()
    user_models.Role.children.property.strategy.join_depth = 0
    return roles

def get_all_authorizations(db : Session):
    return db.query(user_models.Authorization).all()

def create_user(db: Session, create_user: user_serializer.UserCreate) -> user_models.User:
    user = user_models.User()
    db.add(user)
    for k, v in create_user.dict().items():
        setattr(user, k, v)
    db.commit()
    db.refresh(user)
    return user

def patch_user(db : Session, patch_user : user_serializer.UserPatch) -> user_models.User:
    user = get_user_by_id(db, patch_user.id)
    for k, v in patch_user.dict().items():
        if v != None:
            setattr(user, k, v)
    # unset 2FA if requested
    if patch_user.reset_2fa:
        user.totp_secret = None
    db.add(user)
    db.commit()
    return user

def create_role(db: Session, create_role: user_serializer.RoleCreate) -> user_models.Role:
    role = user_models.Role()
    db.add(role)
    for k, v in create_role.dict().items():
        setattr(role, k, v)
    db.commit()
    return role

def delete_role(db : Session, id : int):
    role = get_role_by_id(db, id)
    db.delete(role)
    db.commit()
    return 'Deleted'

def patch_role(db : Session, patch_role : user_serializer.UserPatch) -> user_models.Role:
    role = get_role_by_id(db, patch_role.id)
    for k, v in patch_role.dict().items():
        if v != None:
            setattr(role, k, v)
    db.add(role)
    db.commit()
    return role
