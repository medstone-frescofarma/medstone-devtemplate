from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref

from medstone_backend.db.base_class import Base
from medstone_backend.models.util import TimestampMixin

class Config(Base, TimestampMixin):
    """Stores generic application information"""

    __tablename__ = 'config'
    # primary key
    id                          = Column(Integer, primary_key=True, autoincrement=True)

    # object properties
    key                         = Column(String, nullable=False)
    value                       = Column(String, nullable=False)
