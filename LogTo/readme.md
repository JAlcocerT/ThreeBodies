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


```sh
cd LogTo
python3 logto-sample.py

###

docker compose up --build

#docker compose up --build > compose.log 2>&1
#docker compose up --build | tee compose.log
docker compose up --build flask | tee flask.log
docker compose up --build logto-webhook | tee webhook.log
```


```sh
payload='{"test":123}'
secret='8Cqxy4gGTS1yBegTTkVFFlPi4kxGHVWE'
signature=$(echo -n "$payload" | openssl dgst -sha256 -hmac "$secret" | sed 's/^.* //')
curl -X POST https://webhooks.jalcocertech.com/logto-webhook \
  -H 'Content-Type: application/json' \
  -H "X-Logto-Signature: $signature" \
  -d "$payload"
```