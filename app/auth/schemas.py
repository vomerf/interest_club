import re
from pydantic import BaseModel, EmailStr, Field, model_validator


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str


class RegisterForm(BaseModel):
    username: str
    password: str = Field(..., min_length=8)

    @model_validator(mode='before')
    def validate_password(cls, values):
        password = values.get('password')

        # Проверка на наличие хотя бы одной цифры
        if not re.search(r'\d', password):
            raise ValueError('Password must contain at least one digit')

        # Проверка на наличие хотя бы одной заглавной буквы
        if not re.search(r'[A-Z]', password):
            raise ValueError('Password must contain at least one uppercase letter')

        # Проверка на наличие хотя бы одного символа
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValueError('Password must contain at least one special character !@#$%^&*(),.?":{}|<>')

        return values
