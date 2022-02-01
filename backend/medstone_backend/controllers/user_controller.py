from typing import List

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from medstone_backend.db.deps import get_db
from medstone_backend.serializers import user_serializer
from medstone_backend.services import user_service

router = APIRouter()

@router.get("/", response_model=List[user_serializer.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_service.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/seed")
def seed_users(db: Session = Depends(get_db)):
    user_service.seed_users(db)
    return 'Seeded'
