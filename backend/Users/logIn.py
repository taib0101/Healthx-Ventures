from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from Controller import generateJWT
from MiddleWare import verifyPassword
from main import database, cursor, client

# Depends MiddleWare takes the checker callBack Function
async def logIn(request: Request):

    scope = client.post("/logIn")

    verify = await verifyPassword.verify(cursor)

    requestedData = await request.json()

    accessToken = generateJWT.generateToken(requestedData["userName"])

    return JSONResponse(
        status_code=200,
        content={
            "detail": "User Name and Password okay"
        },
        headers={
            "Authorization": f"Bearer {accessToken}",
            "X-Refresh-Token": accessToken
        }
    )