# main.py
from fastapi import FastAPI, Request, HTTPException, Depends, testclient
from fastapi.responses import JSONResponse
from Model import connection, healthXUser
from Users import logIn
import uvicorn
import json

app = FastAPI()
router = FastAPI().router
client = testclient.TestClient(app)

# Create Connection
database = connection.createConnection()
cursor = database.cursor()

# Read User Table
healthXUser.readAllUser(database, cursor)


@app.post("/signUp")
async def signUp(request: Request):
    try:
        requestedData = await request.json()

        if healthXUser.readSingleUser(cursor, requestedData["userName"]) is not None:
            return JSONResponse(
                status_code=200,
                content={
                    "detail": "User Name Already Exists"
                }
            )

        healthXUser.createUser(database, cursor, True, requestedData)

        return JSONResponse(
            status_code=200,
            content={
                "detail": "User Created SuccessFully"
            }
        )
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data")


# @app.post("/logIn")
# Depends MiddleWare takes the checker callBack Function
# logIn.logIn()


if __name__ == "__main__":
    uvicorn.run("main:app")

    cursor.close()
    database.close()
    print("Database connection closed")
