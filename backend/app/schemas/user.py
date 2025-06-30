"""
用户相关的Pydantic模型
"""

from typing import Optional
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """用户模型"""
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """用户更新模型"""
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None 