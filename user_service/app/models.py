from pydantic import BaseModel, EmailStr, constr
from typing import Optional, Any
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    mobile_number: constr(min_length=10, max_length=15)
    password: constr(min_length=8)
    first_name: str
    last_name: str
    address: Optional[Any] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    mobile_number: Optional[constr(min_length=10, max_length=15)] = None
    password: Optional[constr(min_length=8)] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[Any] = None

class UserOut(BaseModel):
    user_id: UUID
    email: EmailStr
    mobile_number: str
    first_name: str
    last_name: str
    address: Optional[Any] = None
    created_at: datetime
    updated_at: datetime
