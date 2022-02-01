from typing import List

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from medstone_backend.db.deps import get_db
from medstone_backend.serializers import location_serializer, user_serializer
from medstone_backend.services import location_service, auth_service

router = APIRouter()

@router.get("/", response_model=List[location_serializer.Location])
def get_all_locations(
        current_active_user : user_serializer.User = Depends(auth_service.get_current_active_user),
        db: Session = Depends(get_db)
    ):
    return location_service.get_all_locations(db)

@router.get("/seed")
def seed_locations(db: Session = Depends(get_db)):
    location_service.seed_locations(db)
    return 'Seeded'
