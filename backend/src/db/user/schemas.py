from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: str
    gender: Optional[str] = None
    
class UserCreate(UserBase):
    password: str
    faceID: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    gender: Optional[str] = None
    password: Optional[str] = None
    faceID: Optional[str] = None

class UserResponse(UserBase):
    userId: str
    authorizedDevices: Optional[List[str]] = []
    createdAt: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "userId": "user123",
                "username": "johndoe",
                "email": "john.doe@example.com",
                "role": "admin",
                "gender": "male",
                "authorizedDevices": ["device123", "device456"],
                "createdAt": "2023-04-01T12:30:00"
            }
        }

# Common schemas
class ErrorResponse(BaseModel):
    detail: str