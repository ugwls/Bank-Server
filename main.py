from fastapi import FastAPI, Body, Request, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import json

app = FastAPI()
oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/ping")
def home():
    return "Pong"

# Login App Part


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data.username)
    with open("userdb.json", "r") as f:
        json_data = json.load(f)
    if json_data:
        password = json_data.get(form_data.username)
        if not password:
            raise HTTPException(
                status_code=403, detail="Incorrect Username or Password")
            return None
    # To Check if the user name is in the DB and the password matches
    return {
        "access_token": form_data.username,
        "token_type": "bearer"
    }


@app.get("/spend/history")
def spend_history(token: str = Depends(oauth_scheme)):
    print(token)
    print("SPEND History")


@app.get("/creditcard/history")
def credit_history(token: str = Depends(oauth_scheme)):
    print(token)