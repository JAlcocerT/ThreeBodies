from flask import Flask, session, redirect, request, g, jsonify
from typing import Union
from functools import wraps
from logto import LogtoClient, LogtoConfig, Storage, LogtoException

# --- Configuration ---
LOGTO_ENDPOINT = "https://auth.jalcocertech.com/"
LOGTO_APP_ID = "2wgzbimjricwl1nvu94ez"
LOGTO_APP_SECRET = "pbg01D3jJ09IkcyzlThVneXBR5xD02mh"
REDIRECT_URI = "http://192.168.1.11:5088/callback"
POST_LOGOUT_REDIRECT_URI = "http://192.168.1.11:5088/"

# --- Flask App ---
app = Flask(__name__)
app.secret_key = "replace-with-a-secure-random-secret-key"

# --- Logto Session Storage ---
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

# --- Auth Decorator ---
def authenticated(shouldRedirect: bool = False, fetchUserInfo: bool = False):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if client.isAuthenticated() is False:
                if shouldRedirect:
                    return redirect("/sign-in")
                return jsonify({"error": "Not authenticated"}), 401
            # Store user info in Flask application context
            g.user = (
                await client.fetchUserInfo()
                if fetchUserInfo
                else client.getIdTokenClaims()
            )
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# --- Routes ---
@app.route("/")
async def home():
    if client.isAuthenticated() is False:
        return "Not authenticated <a href='/sign-in'>Sign in</a>"
    return "Authenticated <a href='/sign-out'>Sign out</a>"

@app.route("/sign-in")
async def sign_in():
    return redirect(await client.signIn(redirectUri=REDIRECT_URI))

@app.route("/sign-out")
async def sign_out():
    return redirect(await client.signOut(postLogoutRedirectUri=POST_LOGOUT_REDIRECT_URI))

@app.route("/callback")
async def callback():
    try:
        await client.handleSignInCallback(request.url)
        return redirect("/")
    except Exception as e:
        return "Error: " + str(e)

@app.route("/protected/userinfo")
@authenticated(shouldRedirect=True, fetchUserInfo=True)
async def protectedUserinfo():
    try:
        return (
            "<h2>User info</h2>"
            + g.user.model_dump_json(indent=2, exclude_unset=True).replace("\n", "<br>")
        )
    except LogtoException as e:
        return "<h2>Error</h2>" + str(e)

if __name__ == "__main__":
    import os
    import asyncio
    # Run with Hypercorn for async support, but this fallback is for dev/testing only
    port = int(os.environ.get("PORT", 5088))
    try:
        import hypercorn.asyncio
        from hypercorn.config import Config
        config = Config()
        config.bind = [f"192.168.1.11:{port}"]
        asyncio.run(hypercorn.asyncio.serve(app, config))
    except ImportError:
        app.run(host="192.168.1.11", port=port)  # Not async, but helps for quick tests
