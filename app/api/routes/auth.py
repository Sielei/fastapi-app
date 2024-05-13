from fastapi import APIRouter
from app import users_crud
from app.api_models import RegisterUserRequest, RegisterUserResponse, LoginRequest, Token
from app.users_crud import login_user

router = APIRouter()


@router.post("", response_model=RegisterUserResponse)
def register_user(user_in: RegisterUserRequest) -> RegisterUserResponse:
    user = users_crud.register_user(user_in)
    return RegisterUserResponse(user.id)


@router.post("/login")
def login(credential: LoginRequest) -> Token:
    return login_user(credential)
