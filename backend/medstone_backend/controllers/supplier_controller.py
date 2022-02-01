from typing import List

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from medstone_backend.db.deps import get_db
from medstone_backend.serializers import company_serializer, user_serializer
from medstone_backend.services import company_service, auth_service

router = APIRouter()
