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
1. Run openssl
   1. openssl rand -hex 32 
2. For default secret key (only for local testing):
   1. Open core/config.py:
   2. Copy secret key generated in Step 1 
   3. Paste it into
```
class TokenSettings(BaseSettings):
   jwt_local_signature = 'secret key'
```
3. Repeat step 1
   1. Export generated key
      1. export JWT_SIGNATURE=token (generated in Step 3)
      2. At best, you want to put export JWT_SIGNATURE=token in your shell init
         1. For zsh: echo 'export JWT_SIGNATURE=token' >> ~/.zshrc
         2. Then: . ~/.zshrc 
4. Export JWT_EXPIRE_MINUTES=number_of_minutes_for_token_to_expire_since_creation
         
#### IMPORTANT_NOTE:
You can totally skip Step 1 and Step 2 above and go directly to Step 3
even for local testing. Just export your JWT_SIGNATURE.

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