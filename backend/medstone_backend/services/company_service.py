from sqlalchemy.orm import Session

from medstone_backend.models import company_models

def get_all_companies(db: Session):
    return db.query(company_models.company).all()

# def seed_companys(db: Session):
#     companys = create_companys_recursive(companys_default)
#     for d in companys:
#         # Create a new Faker and tell it how to create User objects
#         db.add(d)
#     db.commit()
