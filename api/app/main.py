from fastapi import FastAPI
import uvicorn
from app.routers.health_check import router
from app.core.config import settings


app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run('app.main:app', host=settings.HOST, port=settings.PORT, reload=settings.RELOAD)