from app.celery_app import app


@app.task(queue="reporting")
def hello_task(message: str = "hello") -> dict:
    return {"worker": "reporting-worker", "message": message}
