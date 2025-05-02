from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import ReturnDocument
import logging
from sqlmodel.ext.asyncio.session import AsyncSession
class FaceIDService:
    async def get_faceid_status(self, user: dict, db: AsyncSession):
        """Check if FaceID is enabled for the user"""
        user_id = str(user["_id"])
        user_data = await db["USERS"].find_one({"_id": user_id})
        
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
        
        faceid_enabled = bool(user_data.get("faceID"))
        
        return {
            "success": True,
            "enabled": faceid_enabled
        }

    async def loginface(self, user: dict, db: AsyncSession):
        """Login using FaceID"""
        user_id = str(user["_id"])
        user_data = await db["USERS"].find_one({"_id": user_id})
        
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
        
        if not user_data.get("faceID"):
            raise HTTPException(status_code=400, detail="FaceID not registered")
        
        # Call AI app for FaceID verification
        ai_app_response = await self.call_ai_app_for_login(user_data)
        
        return {
            "message": "FaceID login successful",
            "data": ai_app_response
        }

    async def signupface(self, user: dict, db: AsyncSession):
        """Register FaceID"""
        user_id = str(user["_id"])
        user_data = await db["USERS"].find_one({"_id": user_id})
        
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Call AI app to capture FaceID
        ai_app_response = await self.call_ai_app_for_signup(user_data)
        
        # Save FaceID to MongoDB
        faceid_data = ai_app_response.get("faceID")
        if faceid_data:
            await db["USERS"].update_one(
                {"_id": user_id},
                {"$set": {"faceID": faceid_data}}
            )
        
        return {
            "message": "FaceID registered successfully",
            "data": ai_app_response
        }

    async def call_ai_app_for_login(self, user: dict):
        """Call AI app to verify FaceID"""
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:5001/start-camera-login",
                json={"email": user["email"]}
            )
        response.raise_for_status()
        return response.json()

    async def call_ai_app_for_signup(self, user: dict):
        """Call AI app to enroll FaceID"""
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:5001/start-camera-signup",
                json={"email": user["email"], "password": user["password"]}
            )
        response.raise_for_status()
        return response.json()