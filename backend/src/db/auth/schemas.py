from pydantic import BaseModel, Field


class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)

class UserSignupModel(BaseModel):
    name: str = Field(max_length=100)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)