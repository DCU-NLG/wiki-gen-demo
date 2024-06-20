# WebNLG Demo

## Quick (Dev) Setup
### Backend
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

Lastly, run the app

```shell
flask --app app debug run
```

### Frontend

```shell
cd frontend/
npm install
npm start
```

and open `localhost:3000`.