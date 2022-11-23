from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, constr


class UserBaseSchema(BaseModel):
    name: str = Field(...)
    email: str = Field(...)
    photo: str = Field(None)
    role: str = Field(None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
        


class CreateUserSchema(UserBaseSchema):
    password: constr(min_length=6) = Field(...)
    passwordConfirm: str = Field(...)
    verified: bool = False


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=6)

    class Config:
        schema_extra = {
            "example": {
                "email": "qdatqb@gmail.com",
                "password": "123456",
            }
        }
