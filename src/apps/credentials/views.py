from fastapi import APIRouter
from .urls import USER_CREATE_PATH
import src.database.interaction as db
from src.models.requests import (
    UserDataModel
)
from src.models.responses import (
    UserDataModelResponse
)
router = APIRouter()


@router.post(USER_CREATE_PATH)
def create_new_user(userData: UserDataModel) -> UserDataModelResponse:
    inserted_id = db.create_user(dict(userData))
    return {"status": "OK", "inserted_id": inserted_id}
