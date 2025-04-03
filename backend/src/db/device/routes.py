from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from bson.objectid import ObjectId
from datetime import datetime

from .schemas import (
    DeviceCreate, DeviceResponse, DeviceUpdate, 
)
from .service import DeviceService

router = APIRouter()
device_service = DeviceService()

@router.post("/devices/", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
async def create_device(device: DeviceCreate):
    try:
        result = await device_service.create_device(device)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/devices/", response_model=List[DeviceResponse])
async def get_all_devices(place_id: Optional[str] = None):
    try:
        devices = await device_service.get_all_devices(place_id)
        return devices
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/devices/{device_id}", response_model=DeviceResponse)
async def get_device(device_id: str):
    device = await device_service.get_device_by_id(device_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Device with ID {device_id} not found"
        )
    return device

@router.put("/devices/{device_id}", response_model=DeviceResponse)
async def update_device(device_id: str, device_update: DeviceUpdate):
    updated_device = await device_service.update_device(device_id, device_update)
    if not updated_device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Device with ID {device_id} not found"
        )
    return updated_device

@router.delete("/devices/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(device_id: str):
    deleted = await device_service.delete_device(device_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Device with ID {device_id} not found"
        )
    return None
