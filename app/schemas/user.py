from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str | None = None
    role: str = "cashier"


class UserResponse(BaseModel):
    id: int
    username: str
    full_name: str | None
    role: str
    is_active: bool

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
