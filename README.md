### 1. Design and Implementation

I use FastApi as the backend service to serve quiz building API, and MongoDb to persist
all needed data. To scale well we want to use Cloud Atlas (Mongo DB) cloud. 

To secure API endpoints I use JWT token security.

The main stack is:
Python 3.9.6
FastApi
MongoDb

### 2. App layout / folder / module structure

The app has 5 main folders:

- api
- app
- core
- database
- tests

### 3. Project setup
#### Ensure you have a Python version >= 3.9.6 
You can use pyenv as your Python environment manager, and you
can install a Python version you need.

#### Clone project repo into your local environment
- create a folder to clone the project, say, it is dev/
- cd dev/
- git clone quizapi.gt
- cd quizapi

#### Setup virtual environment and install requirements
- python3 -m venv venv && source ./venv/bin/activate
- pip3 install -r requirements.txt

#### Generate secret (jwt) key and propagate to your local env
Step 1. openssl rand -hex 32 
Step 2. open core/config: 
    A. copy secret key generated in Step 1
    B. paste it into
        class TokenSettings(BaseSettings):
            jwt_local_signature = 'secret key'

#### The config assumes local environment as a default one
You can test in it.

#### Setup cloud Atlas free account
Go to: https://account.mongodb.com/account/login and follow instructions

#### After you created Cloud atlas account create a free cloud atlas cloud
Follow instructions

#### Get a mongodb connection string
Copy it and paste it into core/config.py in MONGODB_CONN_STR='connection_string'

### 4. Unit tests
Unit test coverage is decent and it covers all endpoints.

### Run the server
python3 main.py

### Access swagger docs
Assume you run the server locally, with port=8888
Go to: http://0.0.0.0:8888/docs

You can see all endpoints and you can test them out.

Happy quiz building!