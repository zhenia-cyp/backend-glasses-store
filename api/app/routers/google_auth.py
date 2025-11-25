from fastapi import APIRouter
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from app.core.config import settings

google_router = APIRouter(prefix="/google", tags=["google_auth"])
oauth = OAuth()

oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

@google_router.get('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@google_router.get('/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse(url='/google/test/google/login')


@google_router.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/google/test/google/login')


@google_router.get('/test/google/login')
async def homepage(request: Request):
    user = request.session.get('user')
    if user:
        return HTMLResponse(f"""
            <h1>Привіт, {user.get('name')}!</h1>
            <pre>{user}</pre>
            <br>
            <a href="/logout">Вийти</a>
        """)
    else:
        return HTMLResponse('<a href="/login">Увійти через Google</a>')