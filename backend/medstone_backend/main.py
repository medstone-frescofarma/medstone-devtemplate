from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from medstone_backend.api_v1_router import api_router
from medstone_backend.celery import celery_app

app = FastAPI(
    title="Datastem - Roster Scheduler Webserver",
    description="The backend for Roster Scheduler",
    version="1.0",
    openapi_url="/api/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix='/api/v1')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
