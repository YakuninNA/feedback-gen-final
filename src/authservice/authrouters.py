from fastapi import (
    APIRouter,
    status,
    Request,
    Form,
)
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from starlette.templating import Jinja2Templates
from starlette.responses import (
    Response,
    RedirectResponse
)

from src.authservice.userschemas import (
    UserRegistration,
    UserAuthentication,
)
from src.authservice.usersdao import UsersDAO
from src.authservice.authmanagement import (
    get_hashed_pwd,
    authenticate_user,
    create_access_token
)

router = APIRouter(
    prefix='/new_auth',
    tags=['new_auth']
)


templates = Jinja2Templates(directory="template/auth_templates")


@router.get("/register_form/")
async def get_registration_form(
    request: Request
):
    return templates.TemplateResponse("registration.html", {"request": request})


@router.post("/register_2/")
async def register_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    name: str = Form(...),
    surname: str = Form(...),
    password: str = Form(...)
):
    try:
        user_data = UserRegistration(
            username=username,
            email=email,
            name=name,
            surname=surname,
            hashed_password=password
        )

        hashed_password = get_hashed_pwd(user_data.hashed_password)
        user_dict = user_data.dict()
        user_dict["hashed_password"] = hashed_password
        await UsersDAO.add_instance(**user_dict)

        return templates.TemplateResponse("registration.html", {
            "request": request,
            "message": "You've successfully registered"
        })

    except ValidationError as validation_error:
        error_messages = [err["msg"] for err in validation_error.errors()]
        simplified_message = " ".join(error_messages)
        return templates.TemplateResponse("registration.html", {
            "request": request,
            "error": simplified_message
        })

    except IntegrityError as e:
        error_detail = str(e.orig)
        if "ix_users_email" in error_detail:
            conflict_field = "email"
        else:
            conflict_field = "username"
        return templates.TemplateResponse("registration.html", {
            "request": request,
            "error": f"User with such {conflict_field} already exists"
        })


@router.get("/login")
async def get_login_form(
    request: Request
):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login_2/")
async def auth_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    try:
        user_data = UserAuthentication(
            email=email,
            hashed_password=password,
        )
        check = await authenticate_user(
            email=user_data.email,
            password=user_data.hashed_password,
        )
        if check is None:
            return templates.TemplateResponse(
                "login.html",
                {"request": request, "error": "Wrong email or password"},
                status_code=status.HTTP_400_BAD_REQUEST
            )

        verification_check = await UsersDAO.get_verification_status(email)
        if verification_check is None:
            return templates.TemplateResponse(
                "login.html",
                {"request": request, "error": "Account with this email doesn't exist"},
                status_code=status.HTTP_400_BAD_REQUEST
            )
        if verification_check is False:
            return templates.TemplateResponse(
                "login.html",
                {"request": request, "error": "User with this email is not verified"},
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        access_token = create_access_token(
            {"sub": str(check.id)}
        )
        redirect_response = RedirectResponse(
            status_code=status.HTTP_303_SEE_OTHER,
            url="/functionality/home",
        )
        redirect_response.set_cookie(
            key="users_access_token",
            value=access_token,
            httponly=True
        )

        return redirect_response

    except ValidationError as validation_error:
        error_messages = [err["msg"] for err in validation_error.errors()]
        simplified_message = " ".join(error_messages)
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": simplified_message},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    except ValueError as value_error:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": str(value_error)},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {
        "message": "The user has successfully logged out"
    }

