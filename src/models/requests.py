from pydantic import BaseModel, Field


class UserDataModel(BaseModel):
    username: str = Field(
        description="The login username of the user", default="")
    password: str = Field(
        description="The login password of the user", default="")
