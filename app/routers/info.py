from fastapi import APIRouter, Depends
from ..models import User
from ..schemas import UserResponse
from ..auth import get_current_user

router = APIRouter(prefix="/api")


@router.get("/info", response_model=UserResponse)
def get_user_info(current_user: User = Depends(get_current_user)):
    return current_user
