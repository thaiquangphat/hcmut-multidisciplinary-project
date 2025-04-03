from fastapi import Request, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_token
from fastapi.exceptions import HTTPException


class TokenBearer(HTTPBearer):
    def __init__(self,auto_error = True):
        super().__init__(auto_error=auto_error)


    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = decode_token(token)
        if not self.token_valid(token):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token")
        
   
        
        self.verify_token_data(token_data)
        
        return token_data

    def token_valid(self,token:str) -> bool:
        token_data = decode_token(token)
        
        return token_data is not None 
    
    def verify_token_data(self,token_data):
        raise NotImplementedError('Please Override this method in child classes')


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self,token_data:dict)->None:
        if token_data and token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Please provide access token"
            )
        if 'user' not in token_data or 'user_id' not in token_data['user']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access token does not contain user_id"
            )
        
        user_id = token_data['user']['user_id']
        print(f"Extracted user_id: {user_id}") 
        return user_id

class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self,token_data:dict)->None:
        if token_data and not token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Please provide refresh token"
            )


