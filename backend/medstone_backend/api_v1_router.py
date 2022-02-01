from fastapi import APIRouter

from medstone_backend.controllers import (
    user_controller, auth_controller, common_controller,
    location_controller, supplier_controller)

api_router = APIRouter()
api_router.include_router(user_controller.router, prefix="/users", tags=["users"])
api_router.include_router(auth_controller.router, prefix="/auth", tags=["auth"])
api_router.include_router(common_controller.router, prefix="/common", tags=["common"])
api_router.include_router(location_controller.router, prefix="/location", tags=["location"])
api_router.include_router(supplier_controller.router, prefix="/supplier", tags=["supplier"])
