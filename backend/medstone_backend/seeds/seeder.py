import logging

from sqlalchemy.orm import Session

from medstone_backend.db.deps import session_scope
from medstone_backend.seeds import role_seeder, user_seeder

logger = logging.getLogger(__name__)

def seed_database(db : Session):
    '''Function that seeds our database in case it didn't have specific tables filled'''

    # seed the default roles
    logger.info('Seeding roles')
    role_seeder.seed(db)

    # seed the default users
    logger.info('Seeding users')
    user_seeder.seed(db)


if __name__ == '__main__':
    logger.info('Starting seed process')
    with session_scope() as db:
        seed_database(db)
