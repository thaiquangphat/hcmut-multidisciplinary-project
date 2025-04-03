from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import uuid
from typing import List, Optional, Dict, Any
import bcrypt

from .schemas import  UserCreate, UserUpdate
from ..device.service import DeviceService
from ..main import MongoDB

class UserService(MongoDB):
    def _hash_password(self, password: str) -> str:
        """Hash a password for storing."""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def _verify_password(self, stored_password: str, provided_password: str) -> bool:
        """Verify a stored password against one provided by user"""
        return bcrypt.checkpw(
            provided_password.encode('utf-8'),
            stored_password.encode('utf-8')
        )
    
    async def create_user(self, user: UserCreate) -> Dict[str, Any]:
        existing_user = self.user_collection.find_one({"email": user.email})
        if existing_user:
            raise ValueError(f"User with email {user.email} already exists")
        
        user_id = str(uuid.uuid4())
        
        user_data = user.dict()
        user_data["userId"] = user_id
        user_data["password"] = self._hash_password(user_data["password"])
        user_data["createdAt"] = datetime.now()
        user_data["authorizedDevices"] = []
        
        result = self.user_collection.insert_one(user_data)
        
        if not result.acknowledged:
            raise ValueError("Failed to create user")
            
        user_data["_id"] = str(user_data["_id"])
        return user_data
    
    async def get_all_users(self) -> List[Dict[str, Any]]:
        users = list(self.user_collection.find({}, {"password": 0}))
        
        for user in users:
            if "_id" in user:
                user["_id"] = str(user["_id"])
        
        return users
    
    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        user = self.user_collection.find_one({"userId": user_id}, {"password": 0})
        
        if user:
            if "_id" in user:
                user["_id"] = str(user["_id"])
        
        return user
    
    async def update_user(self, user_id: str, user_update: UserUpdate) -> Optional[Dict[str, Any]]:
        update_data = {k: v for k, v in user_update.dict().items() if v is not None}
        
        if "password" in update_data:
            update_data["password"] = self._hash_password(update_data["password"])
        
        if not update_data:
            return await self.get_user_by_id(user_id)
        
        result = self.user_collection.update_one(
            {"userId": user_id},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            return None
            
        return await self.get_user_by_id(user_id)
    
    async def delete_user(self, user_id: str) -> bool:
        result = self.user_collection.delete_one({"userId": user_id})
        return result.deleted_count > 0
    
    async def authorize_device(self, user_id: str, device_id: str) -> Optional[Dict[str, Any]]:
        user = await self.get_user_by_id(user_id)
        if not user:
            return None
            
        device_service = DeviceService()
        device = await device_service.get_device_by_id(device_id)
        if not device:
            return None
        
        result = self.user_collection.update_one(
            {"userId": user_id},
            {"$addToSet": {"authorizedDevices": device_id}}
        )
        
        if result.matched_count == 0:
            return None
            
        return await self.get_user_by_id(user_id)
    
    async def revoke_device(self, user_id: str, device_id: str) -> Optional[Dict[str, Any]]:
        user = await self.get_user_by_id(user_id)
        if not user:
            return None
        
        result = self.user_collection.update_one(
            {"userId": user_id},
            {"$pull": {"authorizedDevices": device_id}}
        )
        
        if result.matched_count == 0:
            return None
            
        return await self.get_user_by_id(user_id)