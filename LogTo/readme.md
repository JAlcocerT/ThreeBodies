* https://logto.io/
    * https://cloud.logto.io/vurfo6/get-started
    * https://cloud.logto.io/vurfo6/applications/create
* https://docs.logto.io/introduction

```sh
cd LogTo

uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

python3 app-v2.py
```

Step 1: Register Your Flask App in Logto
Log in to your Logto admin console.
Go to Applications and click Create Application.
Choose Regular Web Application.
Set a name, e.g., ThreeBodyApp.
Callback URL:
Add: http://localhost:5000/auth/callback
(or your deployed URL, e.g., https://flask.jalcocertech.com/auth/callback)
Save and note:
Client ID
Client Secret
OIDC Endpoint (e.g., https://<your-logto-domain>/oidc)