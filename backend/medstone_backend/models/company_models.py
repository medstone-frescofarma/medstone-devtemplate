from sqlalchemy import Column, Integer, UnicodeText

from medstone_backend.db.base_class import Base
from medstone_backend.models.util import TimestampMixin

class Company(Base, TimestampMixin):
    '''Stores info on the companies we have'''
    __tablename__ = 'company'
    # primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # object properties
    name = Column(UnicodeText, nullable=False, unique=True)
