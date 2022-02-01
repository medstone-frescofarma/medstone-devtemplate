import logging
from typing import Dict

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from medstone_backend.db.deps import get_db
from medstone_backend.serializers import common_serializer, user_serializer
from medstone_backend.services import user_service, auth_service, location_service

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/", response_model=common_serializer.CommonResponse)
def get_common(
        current_active_user : user_serializer.User = Depends(auth_service.get_current_active_user),
        db: Session = Depends(get_db)
    ):
    logger.info(current_active_user)
    return common_serializer.CommonResponse(
        user=current_active_user,
        locations=location_service.get_all_locations(db)
    )
