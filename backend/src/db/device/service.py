from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import uuid
from typing import List, Optional, Dict, Any
import bcrypt

from .schemas import DeviceCreate, DeviceUpdate
class MongoDB:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017")
        self.db = self.client["QQ"]
        self.device_collection = self.db["record_device"]
        self.user_collection = self.db["user"]

class DeviceService(MongoDB):
    async def create_device(self, device: DeviceCreate) -> Dict[str, Any]:
        # Check if device already exists
        existing_device = await self.get_device_by_id(device.ID)
        if existing_device:
            raise ValueError(f"Device with ID {device.ID} already exists")
        
        device_data = device.dict()
        result = self.device_collection.insert_one(device_data)
        
        if not result.acknowledged:
            raise ValueError("Failed to create device")
            
        return device_data
    
    async def get_all_devices(self, place_id: Optional[str] = None) -> List[Dict[str, Any]]:
        filter_query = {}
        if place_id:
            filter_query["placeID"] = place_id
            
        devices = list(self.device_collection.find(filter_query))
        # Convert ObjectId to string
        for device in devices:
            if "_id" in device:
                device["_id"] = str(device["_id"])
        
        return devices
    
    async def get_device_by_id(self, device_id: str) -> Optional[Dict[str, Any]]:
        device = self.device_collection.find_one({"ID": device_id})
        if device:
            # Convert ObjectId to string
            if "_id" in device:
                device["_id"] = str(device["_id"])
        
        return device
    
    async def update_device(self, device_id: str, device_update: DeviceUpdate) -> Optional[Dict[str, Any]]:
        # Get only non-None fields
        update_data = {k: v for k, v in device_update.dict().items() if v is not None}
        
        if not update_data:
            # No valid fields to update
            return await self.get_device_by_id(device_id)
        
        result = self.device_collection.update_one(
            {"ID": device_id},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            return None
            
        return await self.get_device_by_id(device_id)
    
    async def delete_device(self, device_id: str) -> bool:
        result = self.device_collection.delete_one({"ID": device_id})
        return result.deleted_count > 0
