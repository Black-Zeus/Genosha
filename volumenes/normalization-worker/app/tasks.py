from app.celery_app import app


@app.task(queue="normalization")
def hello_task(message: str = "hello") -> dict:
    return {"worker": "normalization-worker", "message": message}
