import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    # Default to specific auth service callback
    REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8000/auth/google/callback")
    SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-secret-key-for-dev")

    def validate(self):
        if not self.GOOGLE_CLIENT_ID or not self.GOOGLE_CLIENT_SECRET:
            print("WARNING: GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET must be set in .env")

settings = Settings()
settings.validate()
