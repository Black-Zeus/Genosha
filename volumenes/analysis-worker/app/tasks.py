from app.celery_app import app


@app.task(queue="analysis")
def hello_task(message: str = "hello") -> dict:
    return {"worker": "analysis-worker", "message": message}
