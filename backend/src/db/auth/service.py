from src.db.auth.schemas import UserLoginModel, UserSignupModel
from .utils import create_access_token
from passlib.context import CryptContext
from datetime import timedelta
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi import status

REFRESH_TOKEN_EXPIRY = 2
pwd_context = CryptContext(schemes=["bcrypt"])

class LoginService: 
    async def login(self, userdata: UserLoginModel, db) -> JSONResponse:
        try: 
            # Find user by email in the "USERS" collection
            user = await db["USERS"].find_one({"email": userdata.email})
            
            if not user: 
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Wrong email"
                )
            
            if not pwd_context.verify(userdata.password, user["password"]):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Wrong password"
                )
            
            # Use MongoDB's _id as user_id
            user_id = str(user["_id"])
            access_token = create_access_token(
                user_data={'user_id': user_id}
            )
            refresh_token = create_access_token(
                user_data={'user_id': user_id},
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
            )
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Log in successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        'user_id': user_id,
                        'username': user.get("name", "")
                    }
                }
            )
        except HTTPException as e:
            raise e
        except Exception as e: 
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    async def create_new_user(self, user_data: UserSignupModel, db):
        existing_user = await db["USERS"].find_one({"email": user_data.email})
        if existing_user: 
            raise HTTPException(status_code=403, detail="Email already exists")
        
        hashed_password = pwd_context.hash(user_data.password)
        new_user = {
            "name": user_data.name,
            "email": user_data.email,
            "password": hashed_password
        }
        
        result = await db["USERS"].insert_one(new_user)
        if not result.inserted_id:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User creation failed")
        
        return await self.login(UserLoginModel(email=user_data.email, password=user_data.password), db)
