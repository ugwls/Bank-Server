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
    # Spend history logic
    with open('spendhist.json', 'r') as f:
        spend_hist_data = json.load(f)
    if not spend_hist_data.get(token):
        raise HTTPException(
            status_code=403, detail="Username not found in the spend history DB")
    return {
        "Username": token,
        "Spend_hist": spend_hist_data[token]
    }


@app.get("/creditcard/history")
def credit_history(token: str = Depends(oauth_scheme)):
    print(token)
    # Credit Card history logic
    with open('credithist.json', 'r') as f:
        credit_hist_data = json.load(f)
    if not credit_hist_data.get(token):
        raise HTTPException(
            status_code=403, detail="Username not found in the CreditCard history DB")
    return {
        "Username": token,
        "Credit_Hist": credit_hist_data[token]
    }


@app.post("/transfer_money")
def transfer_money(token: str = Depends(oauth_scheme), destination_user: str = Body(...), amount_to_transfer: int = Body(...)):
    print(token)
    print(destination_user)
    print(amount_to_transfer)

    userbalance_data = None
    with open('userbalance.json', 'r') as f:
        userbalance_data = json.load(f)
        # Current user balance
        curr_user_bal = userbalance_data.get(token)['curr_balance']
        print(f'Current User Balance: {curr_user_bal}')
        # destination user balance
        dest_user = userbalance_data.get(destination_user)
        if not dest_user:
            raise HTTPException(
                status_code=400, detail="Destination User is not present in the DB, Cannot transfer money")
        dest_user_bal = dest_user['curr_balance']
        print(f"Destination User Balance: {dest_user_bal}")
        if curr_user_bal - amount_to_transfer < 0:
            raise HTTPException(
                status_code=400, detail="Amount to transfer is greater than account balance. Cannot tranfer money")

    userbalance_data[token]['curr_balance'] -= amount_to_transfer
    print(userbalance_data)
    userbalance_data[destination_user]['curr_balance'] += amount_to_transfer
    with open('userbalance.json', 'w') as f:
        json.dump(userbalance_data, f)
    return {
        "username": token,
        "message": f"Money {amount_to_transfer} succesfully transferd to {destination_user}"
    }


@app.get("/userbalance")
def get_userbalance(token: str = Depends(oauth_scheme)):
    with open('userbalance.json', 'r') as f:
        userbalance = json.load(f)
    if not userbalance.get(token):
        raise HTTPException(
            status_code=400, detail="User not Found.")
    return {
        'Username': token,
        'User Balance': userbalance[token]['curr_balance']
    }
