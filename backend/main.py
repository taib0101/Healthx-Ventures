# main.py
from fastapi import FastAPI, Request, HTTPException
from Model import connection, healthXUser
from Router.Users import logIn, signUp
import uvicorn
import json

app = FastAPI()
router = FastAPI().router

# Create Connection
database = connection.createConnection()
cursor = database.cursor()

# Read User Table
healthXUser.readAllUser(database, cursor)


@app.post("/signUp")
async def signup(request: Request):
    try:
        requestedData = await request.json()
        return signUp.signUp(requestedData)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data")


@app.post("/logIn")
async def login(request: Request):
    try:
        requestedData = await request.json()
        return logIn.logIn(requestedData)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data")
    

@router.get("{userName}/read")
async def usersRead(userName: str, request: Request):
    try:
        requestedData = await request.json()
        requestedHeader = await request.headers()
        
        return logIn.logIn(requestedData)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data")


if __name__ == "__main__":
    uvicorn.run("main:app")

    cursor.close()
    database.close()
    print("Database connection closed")
