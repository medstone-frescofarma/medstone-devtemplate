from apo_bestelportaal_webserver.celery import celery_app

from medstone_backend.db.session import SessionLocal

@celery_app.task(acks_late=True)
def test_task(param : str  = 'world'):
    return f'hello {param}'
