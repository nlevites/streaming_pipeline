import structlog
import uvicorn
from fastapi import FastAPI

from api.ingestion_api.api.routes import api_router

app = FastAPI()
app.include_router(api_router)


@app.on_event("startup")
async def app_startup() -> None:
    logger = structlog.get_logger()
    logger.debug("starting server", database="debug")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
