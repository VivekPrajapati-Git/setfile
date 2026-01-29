from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from ..controllers.auth_controller import AuthController

router = APIRouter()

@router.get("/login/google")
async def login_google(request: Request):
    """
    Redirects the user to the Google OAuth2 authorization URL.
    """
    auth_url = AuthController.get_google_auth_url()
    return RedirectResponse(auth_url)

@router.get("/auth/google/callback")
async def auth_google_callback(request: Request):
    """
    Handle the callback from Google, exchange code for token, and get user info.
    """
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Code not found in request")

    token_json = await AuthController.exchange_code_for_token(code)
    access_token = token_json.get("access_token")
    
    user_info = await AuthController.get_user_info(access_token)
    
    # Store user info in session
    request.session["user"] = user_info
    
    return JSONResponse(content={
        "message": "Login successful",
        "user": user_info,
        "token": token_json
    })

@router.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return {"message": "Logged out"}

@router.get("/me")
async def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user
