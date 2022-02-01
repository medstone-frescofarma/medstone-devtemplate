from celery import Celery

celery_app = Celery("worker", broker="redis://redis/1")
celery_app.conf.task_routes = {
    "*": "default_queue"
}
celery_app.conf.beat_schedule = {
    # 'check-new-bvg-orders': {
    #     'task': 'apo_bestelportaal_webserver.tasks.tasks.check_new_bvg_orders',
    #     'schedule': 60.0,
    # }
}
