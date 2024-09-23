# Seed Wikipedia page generator demo

## Quick (Dev) Setup
### Backend (Python Flask)
Install the required dependencies in a virtual environment
```shell
python -m venv .venv
source .venv/bin/activate 
pip install -r requirements.txt
```

then resolve the submodules

```shell
git submodule update --init --recursive
```

and install p7

```shell
sudo apt install p7zip-full p7zip-rar
```

Create a `env` files under `LLM` and set your aixplain API key

```bash
echo "YOUR-API-KEY" >> .env
```

Lastly, run the app

```shell
flask --app app --debug run
```

### Frontend (ReactJS)

```shell
cd frontend/
npm install
npm start
```

and open `localhost:3000`.
