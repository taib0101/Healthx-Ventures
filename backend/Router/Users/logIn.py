from fastapi import HTTPException
from fastapi.responses import JSONResponse
import main
# from main import database, cursor
from Controller import generateJWT
from MiddleWare import verifyPassword

def logIn(requestedData):

    verifyPassword.verify(main.cursor, requestedData)

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