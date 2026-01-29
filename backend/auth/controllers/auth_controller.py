import httpx
from fastapi import HTTPException
from ..core.config import settings

class AuthController:
    @staticmethod
    def get_google_auth_url():
        if not settings.GOOGLE_CLIENT_ID:
            raise HTTPException(status_code=500, detail="Google Client ID not configured")

        scope = "openid email profile"
        response_type = "code"
        
        auth_url = (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={settings.GOOGLE_CLIENT_ID}&"
            f"response_type={response_type}&"
            f"scope={scope}&"
            f"redirect_uri={settings.REDIRECT_URI}&"
            f"access_type=offline"
        )
        return auth_url

    @staticmethod
    async def exchange_code_for_token(code: str):
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        
        async with httpx.AsyncClient() as client:
            token_response = await client.post(token_url, data=data)
            token_json = token_response.json()
            
            if "error" in token_json:
                raise HTTPException(status_code=400, detail=token_json.get("error_description", "Token exchange failed"))
            
            return token_json

    @staticmethod
    async def get_user_info(access_token: str):
        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        async with httpx.AsyncClient() as client:
            user_response = await client.get(user_info_url, headers=headers)
            user_info = user_response.json()
            return user_info
