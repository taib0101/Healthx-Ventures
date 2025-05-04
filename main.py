# main.py
from fastapi import FastAPI, Request, HTTPException
from Model import connection, healthXUser, healthXUserCRUD
from Router.Users import logIn, signUp
from Router.Users_CRUD import read, create, update, delete
from dotenv import load_dotenv
import uvicorn
import json
import os

app = FastAPI()

# Create Connection
database = connection.createConnection()
cursor = database.cursor()

# Read User Table
healthXUser.readAllUser(database, cursor)
healthXUserCRUD.readAll(database, cursor)


@app.post("/signUp")
async def signup(request: Request):
    try:
        requestedData = await request.json()
        return signUp.signUp(requestedData)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data")
    except Exception:
        raise HTTPException(
            status_code=500, detail="Unexpected error while signup")


"""
@app.post("/{userName}/logIn")
async def login(userName: str, request: Request):
"""


@app.post("/logIn")
async def login(request: Request):
    try:
        requestedData = await request.json()
        return logIn.logIn(requestedData)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data")
    except Exception:
        raise HTTPException(
            status_code=500, detail="Unexpected error while login")


@app.post("/create")
async def userCreate(request: Request):
    try:
        requestedHeader = request.headers
        requestedData = await request.json()
        return create.createData(requestedData, requestedHeader)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data")
    except Exception:
        raise HTTPException(
            status_code=500, detail="Unexpected error while creating user task")


@app.get("/read")
async def usersRead(request: Request):
    try:
        requestedHeader = request.headers
        return read.readData(requestedHeader)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Unexpected error while reading user task")


@app.put("/update")
async def usersUpdate(request: Request):
    try:
        requestedData = await request.json()
        requestedHeader = request.headers
        return update.updateData(requestedData, requestedHeader)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data")
    except Exception:
        raise HTTPException(
            status_code=500, detail="Unexpected error while updating user task")


@app.delete("/delete")
async def usersDelete(request: Request):
    try:
        requestedHeader = request.headers
        return delete.deleteData(requestedHeader)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Unexpected error while updating user task")

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT")), reload=True)
    cursor.close()
    database.close()
    print("Database connection closed")
