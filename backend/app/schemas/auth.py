"""
认证相关的Pydantic模型
"""

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    """访问令牌模型"""
    access_token: str
    token_type: str
    user_id: int
    username: str
    email: str


class UserCreate(BaseModel):
    """用户创建模型"""
    username: str
    email: EmailStr
    password: str
    full_name: str | None = None


class UserLogin(BaseModel):
    """用户登录模型"""
    username: str
    password: str 