from sqlalchemy.orm import Session

from medstone_backend.models import location_models

def get_all_locations(db: Session):
    return db.query(location_models.Location).all()
