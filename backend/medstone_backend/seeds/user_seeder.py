from sqlalchemy.orm import Session

from medstone_backend.models import user_models

def need_to_seed(db : Session) -> bool:
    '''Small utility function that defines if we need to run or not'''
    # check the number of users in the database
    num_users = db.query(user_models.User).count()
    # if we have zero users we need to seed
    return num_users == 0

def seed(db : Session):
    '''A idempotent function to seed if required, else does noting'''
    # check if we should seed
    should_seed = need_to_seed(db)
    if should_seed:
        # define the default users that should exist in the database
        default_users = [
            user_models.User(
                username='koen@vijverb.nl',
                email='koen@vijverb.nl',
                password='koen@vijverb.nl',
                is_admin=True,
                is_active=True
            )
        ]
        for u in default_users:
            db.add(u)
        db.commit()
