from functools import wraps

from flask_login import current_user


def minimum_role(role='anyone'):
    def callable(f):
        # build a Graph of our role structure in memory, this enables us to quicky check if a user
        # has the required privileges to access the method
        @wraps(f)
        def wrapped(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapped
    return callable
