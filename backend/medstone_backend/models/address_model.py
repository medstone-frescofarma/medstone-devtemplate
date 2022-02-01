from sqlalchemy import Column, ForeignKey, Boolean, Integer, Unicode, UnicodeText, DateTime, and_, or_, func
from sqlalchemy.orm import relationship, backref

from medstone_backend.db.base_class import Base
from medstone_backend.models.util import TimestampMixin

class Address(Base, TimestampMixin):
    """Stores address information"""
    __tablename__ = 'address'
    # primary key
    id                  = Column(Integer, primary_key=True, autoincrement=True)

    # object properties
    street_name         = Column(UnicodeText, nullable=True)
    street_number       = Column(UnicodeText, nullable=True)
    city                = Column(UnicodeText, nullable=True)
    zipcode             = Column(UnicodeText, nullable=True)
    country             = Column(UnicodeText, nullable=True)
