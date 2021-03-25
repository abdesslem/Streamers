
# Streamers API

A simple streamers rest API

### Install requirements
```
python3 -m pip install pipenv --user
pipenv install --dev
```
### Setup twitch credentials
```
export CLIENT_ID="<your twitch client id>"
export CLIENT_SECRET="<your twitch client secret"
```
### Run locally
```
pipenv shell && python app.py
```

### Run Test
```
pytest
```

### Build and Run with docker
```
docker build -t streamers-api .
docker run --env CLIENT_ID=<id> --env CLIENT_SECRET=<secret> -d -p 5000:5000 streamers-api
```

