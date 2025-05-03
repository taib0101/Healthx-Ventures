# main.py
from fastapi import FastAPI, Request, HTTPException
from Model import connection, healthXUser, healthXUserCRUD
from Router.Users import logIn, signUp
from Router.Users_CRUD import read, create, update, delete
import uvicorn
import json

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


@app.post("/{userName}/create")
async def userCreate(userName: str, request: Request):
    try:
        requestedHeader = request.headers
        requestedData = await request.json()
        return create.createData(requestedData, requestedHeader)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data")
    except Exception:
        raise HTTPException(
            status_code=500, detail="Unexpected error while creating user task")


@app.get("/{userName}/read")
async def usersRead(userName: str, request: Request):
    try:
        requestedHeader = request.headers
        return read.readData(requestedHeader)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Unexpected error while reading user task")
    
@app.put("/{userName}/update")
async def usersUpdate(userName: str, request: Request):
    try:
        requestedData = await request.json()
        requestedHeader = request.headers
        return update.updateData(requestedData, requestedHeader)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Unexpected error while updating user task")
    
@app.delete("/{userName}/delete")
async def usersDelete(userName: str, request: Request):
    try:
        requestedHeader = request.headers
        return delete.deleteData(requestedHeader)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Unexpected error while updating user task")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
    cursor.close()
    database.close()
    print("Database connection closed")
