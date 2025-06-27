from flask import Flask, session, redirect, request
from typing import Union
from logto import LogtoClient, LogtoConfig, Storage, UserInfoScope

# --- Configuration ---
LOGTO_ENDPOINT = "https://auth.jalcocertech.com/"
LOGTO_APP_ID = "2wgzbimjricwl1nvu94ez"
LOGTO_APP_SECRET = "pbg01D3jJ09IkcyzlThVneXBR5xD02mh"
REDIRECT_URI = "http://192.168.1.11:5088/callback"
POST_LOGOUT_REDIRECT_URI = "http://192.168.1.11:5088/"
#POST_LOGOUT_REDIRECT_URI = "https://fossengineer.com"

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
        scopes=[UserInfoScope.profile, UserInfoScope.email],
    ),
    storage=SessionStorage(),
)

@app.route("/")
async def home():
    if not client.isAuthenticated():
        return redirect("/sign-in")
    userinfo = await client.fetchUserInfo()
    email = getattr(userinfo, 'email', None) or getattr(userinfo, 'primary_email', None)
    verified = getattr(userinfo, 'email_verified', None)
    verified_str = "and your email is <b>verified</b>!" if verified else "but your email is <b>not verified</b>."
    return f"""
        <div style='text-align:center;padding-top:10vh;font-family:Segoe UI,Arial,sans-serif;'>
            <h2>Hello {email or 'user'}!</h2>
            <div style='font-size:1.2em;margin:1em 0;'>You are authenticated {verified_str}</div>
            <a href='/sign-out' style='padding: 14px 32px; font-size: 1.15em; font-weight: 600; border-radius: 32px; background: linear-gradient(90deg,#e684ae,#764ba2,#667eea); color: white; text-decoration: none; box-shadow: 0 4px 24px rgba(118,75,162,0.18); transition: background 0.2s;'>Sign out</a>
        </div>
    """

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

if __name__ == "__main__":
    import os
    import asyncio
    port = int(os.environ.get("PORT", 5088))
    try:
        import hypercorn.asyncio
        from hypercorn.config import Config
        config = Config()
        config.bind = [f"192.168.1.11:{port}"]
        asyncio.run(hypercorn.asyncio.serve(app, config))
    except ImportError:
        app.run(host="192.168.1.11", port=port)
