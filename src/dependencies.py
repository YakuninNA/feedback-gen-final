from fastapi_users import FastAPIUsers

from src.authservice.auth_config import auth_backend
from src.authservice.manager import get_user_manager
from src.authservice.models import User

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)
