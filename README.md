# ThreeBodies

The three body problem with python Flask. Vibe Coded.

```sh
# In your project directory:
docker compose build
docker compose up
```

> Go to `localhost:5000`

![Flask - Three Bodies](Z_DeployMe/3bodes-flask.png)

---

```sh
#python -m venv solvingerror_venv #create the venv
python3 -m venv threebodies_venv #create the venv

#threebodies_venv\Scripts\activate #activate venv (windows)
source threebodies_venv/bin/activate #(linux)
```

**Install dependencies** with:

```sh
#pip install beautifulsoup4 openpyxl pandas numpy==2.0.0
pip install -r requirements.txt #all at once
#pip freeze | grep langchain

#pip show beautifulsoup4
pip list
pip freeze > requirements-output.txt #generate a txt with the ones you have!
```

```sh
source .env

#export OPENAI_API_KEY="your-api-key-here"
#set OPENAI_API_KEY=your-api-key-here
#$env:OPENAI_API_KEY="your-api-key-here"
echo $OPENAI_API_KEY
```