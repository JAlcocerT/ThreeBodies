import asyncio
import os
from flask import Flask, session, redirect, request, g, jsonify
from typing import Union
from functools import wraps
from logto import LogtoClient, LogtoConfig, Storage, LogtoException, UserInfoScope

# --- Load environment variables from .env if present ---
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # If python-dotenv is not installed, skip loading .env

# --- Configuration from environment variables or fallback defaults ---
LOGTO_ENDPOINT = os.environ.get("LOGTO_ENDPOINT", "https://auth.jalcocertech.com/")
LOGTO_APP_ID = os.environ.get("LOGTO_APP_ID", "2wgzbimjricwl1nvu94ez")
LOGTO_APP_SECRET = os.environ.get("LOGTO_APP_SECRET", "pbg01D3jJ09IkcyzlThVneXBR5xD02mh")
REDIRECT_URI = os.environ.get("REDIRECT_URI", "http://192.168.1.11:5088/callback")
POST_LOGOUT_REDIRECT_URI = os.environ.get("POST_LOGOUT_REDIRECT_URI", "http://192.168.1.11:5088")
FLASK_SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "replace-with-a-secure-random-secret-key")

# --- Flask App ---
app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY

# --- Logto Session Storage ---
class SessionStorage(Storage):
    def get(self, key: str) -> Union[str, None]:
        return session.get(key, None)
    def set(self, key: str, value: Union[str, None]) -> None:
        session[key] = value
    def delete(self, key: str) -> None:
        session.pop(key, None)

# --- Logto Client with additional scopes ---
client = LogtoClient(
    LogtoConfig(
        endpoint=LOGTO_ENDPOINT,
        appId=LOGTO_APP_ID,
        appSecret=LOGTO_APP_SECRET,
        scopes=[UserInfoScope.email, UserInfoScope.profile],
    ),
    storage=SessionStorage(),
)

# --- Authenticated decorator ---
def authenticated(shouldRedirect: bool = False, fetchUserInfo: bool = False):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not client.isAuthenticated():
                if shouldRedirect:
                    return redirect("/sign-in")
                return jsonify({"error": "Not authenticated"}), 401
            g.user = await client.fetchUserInfo() if fetchUserInfo else client.getIdTokenClaims()
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# --- Routes ---
@app.route("/")
async def home():
    is_auth = client.isAuthenticated()
    userinfo_html = ""
    if is_auth:
        userinfo = await client.fetchUserInfo()
        name = getattr(userinfo, 'name', None)
        email = getattr(userinfo, 'email', None) or getattr(userinfo, 'primary_email', None)
        username = getattr(userinfo, 'username', None)
        userinfo_html = f"""
            <div style='margin-top:1em;font-size:1.1em;color:#444;'>
                <div><b>Name:</b> {name or '-'}<br></div>
                <div><b>Email:</b> {email or '-'}<br></div>
                <div><b>Username:</b> {username or '-'}<br></div>
                <div style='margin-top:1em;'><a href='/protected/userinfo' style='font-size:1em;'>View all user info (JSON)</a></div>
            </div>
        """
    user_html = """
        <div style='text-align:center;'>
            <h2 style='margin-bottom:0.5em;'>Welcome to Logto Sample App!</h2>
            <p style='margin-top:0;'>This is a demo Python Flask app with Logto authentication.</p>
        </div>
    """
    button_html = """
        <div style='position:absolute;top:32px;right:32px;'>
            <a href='/sign-in' style='padding: 14px 32px; font-size: 1.15em; font-weight: 600; border-radius: 32px; background: linear-gradient(90deg,#667eea,#764ba2,#e684ae); color: white; text-decoration: none; box-shadow: 0 4px 24px rgba(118,75,162,0.18); transition: background 0.2s;'>Sign in / Sign up</a>
        </div>
    """
    signout_html = """
        <div style='position:absolute;top:32px;right:32px;'>
            <a href='/sign-out' style='padding: 14px 32px; font-size: 1.15em; font-weight: 600; border-radius: 32px; background: linear-gradient(90deg,#e684ae,#764ba2,#667eea); color: white; text-decoration: none; box-shadow: 0 4px 24px rgba(118,75,162,0.18); transition: background 0.2s;'>Sign out</a>
        </div>
    """
    bg_style = """
        <style>
            body {
                min-height: 100vh;
                margin: 0;
                font-family: 'Segoe UI', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #e684ae 100%);
                color: #222;
            }
            .centered {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: flex-start;
                min-height: 100vh;
                padding-top: 10vh;
            }
        </style>
    """
    html = f"""
        <!DOCTYPE html>
        <html lang='en'>
        <head>
            <meta charset='utf-8'>
            <title>Logto Sample App</title>
            {bg_style}
        </head>
        <body>
            {button_html if not is_auth else signout_html}
            <div class='centered'>
                {user_html}
                {userinfo_html}
                <div style='margin-top:2em;font-size:1.1em;'>
                    {'You are <b>not authenticated</b>.' if not is_auth else 'You are <b>authenticated</b>!'}
                </div>
            </div>
        </body>
        </html>
    """
    return html


@app.route("/sign-in")
async def sign_in():
    return redirect(await client.signIn(redirectUri=REDIRECT_URI))

@app.route("/callback")
async def callback():
    code = request.args.get("code")
    if not code:
        return "Missing code", 400
    await client.handleSignInCallback(code, redirectUri=REDIRECT_URI)
    return redirect("/")

@app.route("/sign-out")
async def sign_out():
    return redirect(await client.signOut(postLogoutRedirectUri=POST_LOGOUT_REDIRECT_URI))

@app.route("/protected/userinfo")
@authenticated(shouldRedirect=True, fetchUserInfo=True)
async def protected_userinfo():
    try:
        return (
            "<h2>User info</h2>"
            + g.user.model_dump_json(indent=2, exclude_unset=True).replace("\n", "<br>")
            + "<br><a href='/'>Home</a>"
        )
    except LogtoException as e:
        return "<h2>Error</h2>" + str(e) + "<br><a href='/'>Home</a>"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5088))
    app.run(host="0.0.0.0", port=port, debug=True)
