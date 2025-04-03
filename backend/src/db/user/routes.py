from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from bson.objectid import ObjectId
from datetime import datetime

from .schemas import (
    UserCreate, UserResponse, UserUpdate,
    ErrorResponse
)
from .service import UserService
router = APIRouter()

user_service = UserService()

@router.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    try:
        result = await user_service.create_user(user)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/users/", response_model=List[UserResponse])
async def get_all_users():
    try:
        users = await user_service.get_all_users()
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user_update: UserUpdate):
    updated_user = await user_service.update_user(user_id, user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return updated_user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    deleted = await user_service.delete_user(user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return None

@router.post("/users/{user_id}/authorize-device/{device_id}", response_model=UserResponse)
async def authorize_device(user_id: str, device_id: str):
    user = await user_service.authorize_device(user_id, device_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} or device with ID {device_id} not found"
        )
    return user

@router.delete("/users/{user_id}/revoke-device/{device_id}", response_model=UserResponse)
async def revoke_device(user_id: str, device_id: str):
    user = await user_service.revoke_device(user_id, device_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} or device with ID {device_id} not found"
        )
    return user