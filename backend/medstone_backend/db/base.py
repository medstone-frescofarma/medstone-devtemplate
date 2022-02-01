# Import all the models, so that Base has them before being
# imported by Alembic
from medstone_backend.db.base_class import Base  # noqa
from medstone_backend.models.address_model import Address
from medstone_backend.models.user_models import User  # noqa
from medstone_backend.models.location_models import Location
from medstone_backend.models.company_models import Company
