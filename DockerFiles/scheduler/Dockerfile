FROM python:3.12-slim
WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código montado como bind-mount → hot-reload via watchfiles
CMD ["watchfiles", "celery -A app.celery_app beat --loglevel=info", "app/"]
