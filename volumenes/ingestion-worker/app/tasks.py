from app.celery_app import app


@app.task(queue="ingestion")
def hello_task(message: str = "hello") -> dict:
    return {"worker": "ingestion-worker", "message": message}
