from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from .core.config import settings
from .routes import auth_routes

app = FastAPI(title="Auth Service")

# Add Session Middleware
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# Include Router
app.include_router(auth_routes.router)

@app.get("/")
async def root():
    return {"message": "Google Auth Service is running. Go to /login/google to login."}
