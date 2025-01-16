from adminpanel.adminschemas import (
    UserStatusChange,
    UserVerification
)
from adminpanel.adminsdao import AdminsDAO
from fastapi import (
    APIRouter,
    status,
    Depends,
    Request,
    HTTPException
)
from pydantic import ValidationError
from starlette.templating import Jinja2Templates

from src.authservice.models import User
from src.authservice.dependencies import get_current_admin_user


router = APIRouter(
    prefix='/admin_panel',
    tags=['Admin_panel']
)


templates = Jinja2Templates(directory="template/auth_templates")


@router.put("/get_user_status")
async def get_user_status(
        email: str,
        field: str,
        request: Request,
        admin_user_data: User = Depends(get_current_admin_user)
):
    try:
        user_data = UserVerification(
            email=email,
            verification_field=field
        )

        any_status = await AdminsDAO.get_any_status(
            user_data.email,
            user_data.verification_field
        )

        return any_status

    except AttributeError:
        raise ValueError(f"Field '{field}' does not exist in the model")


@router.put("/change_user_status")
async def change_user_status(
        email: str,
        field: str,
        desired_val: bool,
        request: Request,
        admin_user_data: User = Depends(get_current_admin_user)
):
    try:
        user_data = UserStatusChange(
            email=email,
            db_field=field,
            status_field=desired_val
        )

        verification_check = await AdminsDAO.get_any_status(
            user_data.email,
            user_data.db_field
        )
        if verification_check == user_data.status_field:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{user_data.db_field} remained {verification_check} for user {user_data.email}"
            )
        if verification_check is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User {user_data.email} doesn't exist"
            )

        await AdminsDAO.change_user_status(
            email=user_data.email,
            desired_field=user_data.db_field,
            desired_value=user_data.status_field
        )

        return {
            "status": "success",
            "message": f"{user_data.db_field} has been set to {user_data.status_field} for user {user_data.email}"
        }

    except ValidationError as val_err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(val_err)
        )

    except ValueError as value_error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(value_error)
        )

    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(f"Field '{field}' does not exist in the model")
        )
