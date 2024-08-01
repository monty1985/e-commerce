from pydantic import BaseModel, EmailStr, constr, model_validator
from typing import Optional, Any, Union
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Union[str, None] = None

class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
    mobile_number: constr(min_length=10, max_length=15)
    first_name: str
    last_name: str
    address: Optional[Any] = None
    auth_provider: Optional[str] = None
    provider_id: Optional[str] = None

class UserOut(BaseModel):
    user_id: str
    email: EmailStr
    mobile_number: str
    first_name: str
    last_name: str
    address: Optional[Any] = None
    created_at: datetime
    updated_at: datetime
    auth_provider: Optional[str] = None
    provider_id: Optional[str] = None

    @model_validator(mode='before')
    def set_user_id(cls, values):
        if isinstance(values, dict):
            values['user_id'] = values.get('id')
        else:
            values.user_id = values.id
        return values

    class Config:
        orm_mode = True
        from_attributes = True
