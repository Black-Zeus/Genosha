from fastapi import FastAPI

app = FastAPI(title="Genosha API", version="0.1.0")


@app.get("/api/v1/health")
def health():
    return {"status": "ok", "service": "genosha-api"}


@app.get("/")
def root():
    return {"message": "Genosha API"}
