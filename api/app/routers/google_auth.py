from fastapi import APIRouter, Depends, status
from authlib.integrations.starlette_client import OAuth, OAuthError
from starlette.requests import Request
from starlette.responses import RedirectResponse, HTMLResponse
from app.core.config import settings
from app.core.templates import templates
from app.services.auth import AuthService, get_auth_service
from app.services.users import UserService, get_user_service



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
async def auth(
    request: Request,
    user_service: UserService = Depends(get_user_service),
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        error_url = f"{settings.OAUTH_FAILURE_REDIRECT_URL}?error={error.error}"
        return RedirectResponse(url=error_url)

    user_info = token.get('userinfo') or {}
    email = user_info.get('email')

    if not email or '@' not in email:
        error_url = f"{settings.OAUTH_FAILURE_REDIRECT_URL}?error=no_email"
        return RedirectResponse(url=error_url)

    try:
        user = await user_service.create_or_update_from_oauth(
            email=email,
            firstname=user_info.get('given_name') or user_info.get('name'),
            lastname=user_info.get('family_name'),
            phone=user_info.get('phone_number'),
        )

        _, refresh_token = await auth_service.issue_tokens_for_email(user.email)
    except Exception as e:
        error_url = f"{settings.OAUTH_FAILURE_REDIRECT_URL}?error=server_error"
        return RedirectResponse(url=error_url)

    response = templates.TemplateResponse(
        "oauth_callback.html",
        {
            "request": request,
            "redirect_url": settings.OAUTH_SUCCESS_REDIRECT_URL,
        }
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        secure=not settings.DEBUG,
        max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
    )
    return response


@google_router.get('/test/success/router')
async def homepage(request: Request):
        return HTMLResponse(f"""
        <h1>Google OAuth2 Successful</h1>
           """)


@google_router.get('/logout')
async def logout():
    response = RedirectResponse(
        url=settings.OAUTH_SUCCESS_REDIRECT_URL,
        status_code=status.HTTP_302_FOUND,
    )
    response.delete_cookie("refresh_token")
    return response