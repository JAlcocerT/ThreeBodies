import asyncio
import os
from flask import Flask, session, request, redirect, g
from logto import LogtoClient, LogtoConfig, Storage
from typing import Union
from functools import wraps
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "uUbY6uEuqmBFI53e")

# --- Logto Config --- # https://cloud.logto.io/
LOGTO_ENDPOINT = os.environ.get("LOGTO_ENDPOINT", "https://notto.logto.app/")
LOGTO_APP_ID = os.environ.get("LOGTO_APP_ID", "write")
LOGTO_APP_SECRET = os.environ.get("LOGTO_APP_SECRET", "secretshere")
REDIRECT_URI = os.environ.get("REDIRECT_URI", "http://localhost:5050/callback")
##hypercorn app-v2:app --bind 0.0.0.0:5050


from logto import LogtoClient, LogtoConfig

# client = LogtoClient(
#     LogtoConfig(
#         endpoint="https://vurfo6.logto.app/",
#         appId="9ca8tbt26nfcxg2x5m0z8",
#         appSecret="DSVbSh6M3P8o8ylm93ZkfecCTFI1j70b",
#     )
# )

class SessionStorage(Storage):
    def get(self, key: str) -> Union[str, None]:
        return session.get(key, None)
    def set(self, key: str, value: Union[str, None]) -> None:
        session[key] = value
    def delete(self, key: str) -> None:
        session.pop(key, None)

client = LogtoClient(
    LogtoConfig(
        endpoint=LOGTO_ENDPOINT,
        appId=LOGTO_APP_ID,
        appSecret=LOGTO_APP_SECRET,
    ),
    storage=SessionStorage(),
)

def authenticated(shouldRedirect: bool = False, fetchUserInfo: bool = False):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not client.isAuthenticated():
                if shouldRedirect:
                    return redirect("/sign-in")
                return "Not authenticated", 401
            g.user = (
                await client.fetchUserInfo() if fetchUserInfo else client.getIdTokenClaims()
            )
            return await func(*args, **kwargs)
        return wrapper
    return decorator

@app.route("/")
async def home():
    if not client.isAuthenticated():
        return "Not authenticated <a href='/sign-in'>Sign in</a>"
    userinfo = await client.fetchUserInfo()
    # Try primary_email (native Logto user)
    email = getattr(userinfo, "primary_email", None)
    # Try social identity providers if not found
    if not email and hasattr(userinfo, "identities"):
        identities = userinfo.identities
        if isinstance(identities, dict):
            for ident in identities.values():
                details = getattr(ident, "details", None)
                if details and hasattr(details, "email"):
                    email = details.email
                    break
    if not email:
        email = "Unknown"
    return f"Hi {email}, you are authenticated! <a href='/sign-out'>Sign out</a>"

@app.route("/sign-in")
async def sign_in():
    return redirect(await client.signIn(redirectUri=REDIRECT_URI))

@app.route("/sign-out")
async def sign_out():
    return redirect(await client.signOut(postLogoutRedirectUri="http://localhost:5000/"))

@app.route("/callback")
async def callback():
    try:
        await client.handleSignInCallback(request.url)
        return redirect("/")
    except Exception as e:
        return "Error: " + str(e)

@app.route("/protected/userinfo")
@authenticated(shouldRedirect=True, fetchUserInfo=True)
async def protected_userinfo():
    return f"<h2>User info</h2>{g.user.model_dump_json(indent=2, exclude_unset=True).replace(chr(10), '<br>')}"

if __name__ == "__main__":
    # Flask's built-in server does not support async, so use Hypercorn or another ASGI server for async support:
    # pip install hypercorn
    # Run: hypercorn app-v2:app
    import os
    os.system("hypercorn app-v2:app")