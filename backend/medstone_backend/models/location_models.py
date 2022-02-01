import datetime

from sqlalchemy import Column, ForeignKey, Integer, UnicodeText
from sqlalchemy.orm import relationship, backref

from medstone_backend.db.base_class import Base
from medstone_backend.models.util import TimestampMixin

class Location(Base, TimestampMixin):
    """Stores the locations we have"""
    __tablename__ = 'location'
    # primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # forein keys
    company_id      = Column(Integer, ForeignKey('company.id'), nullable=False)
    parent_id       = Column(Integer, ForeignKey('location.id'), nullable=True)

    # object properties
    name            = Column(UnicodeText, nullable=False, unique=True)
    description     = Column(UnicodeText, nullable=True)

    # relationships
    children        = relationship('Location', backref=backref('parent', remote_side=[id]))
