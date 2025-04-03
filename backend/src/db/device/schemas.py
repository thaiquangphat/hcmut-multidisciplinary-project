from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime

class Temperature(BaseModel):
    time: datetime
    value: float

class DeviceBase(BaseModel):
    Humidity: float
    Light: float
    Temperature: Temperature
    placeID: str

class DeviceCreate(DeviceBase):
    ID: str

class DeviceUpdate(BaseModel):
    Humidity: Optional[float] = None
    Light: Optional[float] = None
    Temperature: Optional[Temperature] = None
    placeID: Optional[str] = None

class DeviceResponse(DeviceBase):
    ID: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "ID": "device123",
                "Humidity": 45.7,
                "Light": 800.5,
                "Temperature": {
                    "time": "2023-04-01T12:30:00",
                    "value": 23.5
                },
                "placeID": "livingroom"
            }
        }
