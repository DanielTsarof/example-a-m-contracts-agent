import uvicorn
from fastapi import FastAPI
from api.v1.api import api_router
from logger import log
from config import config

app = FastAPI(title="M&A Agent (demo)")
app.include_router(api_router)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

if __name__ == "__main__":
    log.info("Starting server...")
    uvicorn.run(
        "main:app",
        host=config.uvicorn.ip,
        port=config.uvicorn.port,
        reload=config.uvicorn.enable_auto_reload,
        log_level=config.uvicorn.log_level,
    )
