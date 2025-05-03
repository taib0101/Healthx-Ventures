from fastapi import HTTPException
from fastapi.responses import JSONResponse
import main
from Controller import generateJWT
from MiddleWare import verifyPassword


def logIn(requestedData):
    try:
        verify = verifyPassword.verify(main.cursor, requestedData)

        print("verify: ", verify)

        if verify is False:
            return JSONResponse(
                status_code=401,
                content={
                    "detail": "Unauthorized , User or Password Invalid"
                }
            )

        accessToken = generateJWT.generateToken(requestedData["userName"])

        return JSONResponse(
            status_code=200,
            content={
                "detail": "User Name and Password okay"
            },
            headers={
                "Authorization": f"Bearer {accessToken}",
                "token": accessToken
            }
        )
    except Exception:
        raise HTTPException(
            status_code=500, detail="Unexpected error while login")
