import re
from pydantic import BaseModel, EmailStr, Field, model_validator, EmailStr
from typing import Optional


def validate_password_strength(password: str) -> list[str]:
    errors = []
    if not re.search(r'\d', password):
        errors.append('Пароль должен содержать хотя бы одну цифру')
    if not re.search(r'[A-Z]', password):
        errors.append('Пароль должен содержать хотя бы одну заглавную букву')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append('Пароль должен содержать хотя бы один специальный символ')
    return errors


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
        """Проверка пароля."""
        if data['password'] != data['confirm_password']:
            raise ValueError('Пароли не совпадают')

        errors = validate_password_strength(data['password'])
        if errors:
            raise ValueError(errors)
        return data

    @model_validator(mode='before')
    def validate_phone(cls, data):
        """Проверка телефона (только для России)."""
        phone = data.get('phone')
        if phone:
            # Регулярное выражение для российских номеров
            phone_pattern = re.compile(r'^(?:\+7|8)?\d{10}$')
            if not phone_pattern.match(phone):
                raise ValueError(
                    'Телефон должен быть в формате российского номера (пример: +79161234567 или 89161234567)'
                )
        return data
