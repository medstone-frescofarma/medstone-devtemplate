from typing import Generator
from contextlib import contextmanager

from medstone_backend.db.session import SessionLocal

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    db = SessionLocal()
    try:
        yield db
    except:
        raise
    finally:
        db.close()
