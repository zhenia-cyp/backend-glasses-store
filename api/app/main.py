from fastapi import FastAPI
import uvicorn
from app.routers.health_check import router
from app.core.config import settings
from app.routers.users import user_router

app = FastAPI()
app.include_router(router)
app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run('app.main:app', host=settings.HOST, port=settings.PORT, reload=settings.RELOAD)