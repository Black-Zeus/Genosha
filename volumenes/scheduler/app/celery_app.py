import os
from celery import Celery
from celery.schedules import crontab

app = Celery(
    "genosha-scheduler",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1"),
    include=["app.tasks"],
)

app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

app.conf.beat_schedule = {
    "heartbeat-every-minute": {
        "task": "app.tasks.heartbeat",
        "schedule": crontab(minute="*"),
    },
}
