from fastapi import APIRouter, Request, Depends, status, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_users.authentication import Strategy
from fastapi_users.exceptions import UserAlreadyExists
from fastapi.security import OAuth2PasswordRequestForm

from src.authservice.auth_config import auth_backend, get_jwt_strategy
from src.authservice.manager import get_user_manager, UserManager
from src.authservice.schemas import UserCreate
from src.dependencies import current_active_user, fastapi_users

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

templates = Jinja2Templates(directory="template/auth_templates")


@router.get("/home")
def get_base_page(request: Request):
    return templates.TemplateResponse(
        "home_page.html",
        {"request": request})


@router.get("/registration", response_class=HTMLResponse)
async def get_registration_form(
    request: Request,
    user=Depends(fastapi_users.current_user(optional=True))
):
    return templates.TemplateResponse("registration.html", {"request": request, "user": user})


@router.post("/registration", response_class=HTMLResponse)
async def custom_register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    name: str = Form(...),
    surname: str = Form(...),
    user_manager: UserManager = Depends(get_user_manager)
):
    user_create = UserCreate(
        username=username,
        email=email,
        password=password,
        name=name,
        surname=surname,
    )

    try:
        await user_manager.create(user_create)
        return templates.TemplateResponse("success_auth.html", {"request": request})
    except UserAlreadyExists:
        return templates.TemplateResponse(
            "registration.html",
            {"request": request, "error": "User already exists"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    except Exception as e:
        print(f"Error during registration: {e}")
        return templates.TemplateResponse(
            "registration.html",
            {"request": request, "error": "An unexpected error occurred"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/login", response_class=HTMLResponse)
async def get_login_form(
    request: Request,
    user=Depends(fastapi_users.current_user(optional=True))
):
    return templates.TemplateResponse("login.html", {"request": request, "user": user})


@router.post("/login")
async def custom_login(
        request: Request,
        form_data: OAuth2PasswordRequestForm = Depends(),
        user_manager: UserManager = Depends(get_user_manager),
        strategy: Strategy = Depends(get_jwt_strategy)
):
    try:
        user = await user_manager.authenticate(form_data)

        if user is None:
            return templates.TemplateResponse(
                "login.html",
                {"request": request, "error": "Invalid username or password."},
                status_code=status.HTTP_400_BAD_REQUEST
            )
        login_response = await auth_backend.login(strategy, user)
        response = RedirectResponse(url="/functionality/home", status_code=status.HTTP_303_SEE_OTHER)
        set_cookie_header = login_response.headers.get('set-cookie')

        if set_cookie_header:
            response.headers['set-cookie'] = set_cookie_header
        response.set_cookie(key="is_authenticated", value="true")

        return response

    except Exception as e:
        print(f"Error during login: {e}")
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "An error occurred during login."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.post("/logout")
async def logout(
        request: Request,
        user=Depends(current_active_user),
):
    redirect_response = RedirectResponse(url="/auth/home", status_code=status.HTTP_302_FOUND)

    redirect_response.delete_cookie(key="auth")
    redirect_response.delete_cookie(key="is_authenticated")

    return redirect_response


