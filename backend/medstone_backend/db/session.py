from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from medstone_backend.config import config

if 'postgresql' in config.SQLALCHEMY_DATABASE_URI:
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
else:
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, connect_args={ 'check_same_thread': False })
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
