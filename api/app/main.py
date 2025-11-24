from fastapi import FastAPI
import uvicorn
from app.routers.health_check import router
from app.core.config import settings
from app.routers.users import user_router
from app.routers.auth import auth_router


app = FastAPI()
app.include_router(router)
app.include_router(user_router)
app.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run('app.main:app', host=settings.HOST, port=settings.PORT, reload=settings.RELOAD)