from app.celery_app import app


@app.task(queue="vector")
def hello_task(message: str = "hello") -> dict:
    return {"worker": "vector-worker", "message": message}
