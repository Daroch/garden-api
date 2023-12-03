import os


class Config:
    CELERY_BROKER_URL: str = os.environ.get(
        "CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
    CELERY_RESULT_BACKEND: str = os.environ.get(
        "CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0")
    CELERY_TASK_ROUTES: dict = {
        'tasks.*': {
            'queue': 'high_priority',
        },
        'low_priority_tasks.*': {
            'queue': 'low_priority',
        },
    }

    # new
    CELERY_BEAT_SCHEDULE: dict = {
        "send_credit_report": {
            "task": "credit_report",
            "schedule": 10,
            'options': {'queue': 'periodic'},
        },
    }
    CELERY_TIMEZONE: str = "US/Mountain"


settings = Config()
