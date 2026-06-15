from datetime import datetime, timezone
from app.celery_app import app


@app.task
def heartbeat() -> dict:
    return {"status": "alive", "timestamp": datetime.now(timezone.utc).isoformat()}
