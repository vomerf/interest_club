import re
from pydantic import BaseModel, EmailStr, Field, model_validator, EmailStr
from typing import Optional


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
    name: str
    lastname: str
    username: str = Field(..., min_length=3, max_length=30)
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
    email: EmailStr
    phone: Optional[str]

    @model_validator(mode='before')
    def check_passwords_match(cls, data):
        if data['password'] != data['confirm_password']:
            raise ValueError('Пароли не совпадают')

        if not re.search(r'\d', data['password']):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')

        if not re.search(r'[A-Z]', data['password']):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', data['password']):
            raise ValueError('Пароль должен содержать хотя бы один специальный символ')
        return data
