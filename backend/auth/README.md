# Auth Service

This is a dedicated microservice for handling Google Authentication.

## Structure

```text
auth/
├── controllers/    # Business logic (OAuth2 flow)
├── routes/         # FastAPI endpoints
├── core/           # Configuration & Settings
├── .env            # Environment variables
├── requirements.txt
├── main.py         # App entry point
└── __main__.py     # Script to run module directly
```

## Setup

1.  **Install Dependencies:**
    ```bash
    pip install -r auth/requirements.txt
    ```

2.  **Environment Variables:**
    Ensure `auth/.env` exists with the following:
    ```env
    GOOGLE_CLIENT_ID=your_client_id
    GOOGLE_CLIENT_SECRET=your_client_secret
    SECRET_KEY=your_secret_key
    REDIRECT_URI=http://localhost:8000/auth/google/callback
    ```

## Running the Service

From the `backend/` directory, run:

```bash
python auth
```

The service will start on `http://127.0.0.1:8000`.

## Endpoints

*   `GET /login/google`: Initiates the Google OAuth2 login flow.
*   `GET /auth/google/callback`: Callback URL handling token exchange.
*   `GET /me`: Returns the currently authenticated user's profile.
*   `GET /logout`: Clears the session.
