from sqlalchemy.orm import Session

from medstone_backend.models import user_models

def need_to_seed(db : Session) -> bool:
    '''Small utility function that defines if we need to run or not'''
    # check the number of roles in the database
    num_roles = db.query(user_models.Role).count()
    # we need to run if we have no roles
    return num_roles == 0

def seed(db : Session):
    '''A idempotent function to seed if required, else does noting'''
    # check if we should seed
    should_seed = need_to_seed(db)
    if should_seed:
        # define the default roles that should exist in the database
        manager_role = user_models.Role(
            name='Manager',
            description='Can manage users / employees and scheduling'
        )
        db.add(manager_role)
        employee_role = user_models.Role(
            name='Employee',
            description='Can view own roster and fill out personal preferences for scheduling'
        )
        db.add(employee_role)
        db.commit()
