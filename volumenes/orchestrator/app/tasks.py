from app.celery_app import app


@app.task(queue="orchestration")
def hello_task(message: str = "hello") -> dict:
    return {"worker": "orchestrator", "message": message}
