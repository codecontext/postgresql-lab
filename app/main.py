from fastapi import FastAPI

app = FastAPI(title="PostgreSQL Learning Lab")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}