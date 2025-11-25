from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
from app.routers.health_check import router
from app.core.config import settings
from app.routers.users import user_router
from app.routers.auth import auth_router
from app.routers.google_auth import google_router

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET_KEY
)

app.include_router(router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(google_router)


if __name__ == "__main__":
    uvicorn.run('app.main:app', host=settings.HOST, port=settings.PORT, reload=settings.RELOAD)