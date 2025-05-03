from fastapi.responses import JSONResponse
from Controller import JWTCheck
from Model import healthXUserCRUD
import main

def updateData(requestedHeader):
    token = requestedHeader["token"]
    checkJWT = JWTCheck.check_jwt_expiry(token)

    if checkJWT["valid"] is False:
        return JSONResponse(
            status_code=401,
            content={
                "detail": "Expire or Invalid Token"
            }
        )

    userName = checkJWT["payload"]["userName"]
    id = requestedHeader["id"]
    healthXUserCRUD.updateSingleUserTask(main.cursor, userName, id)
    return JSONResponse(
        status_code=200,
        content={
            "detail": "Readed Successfully"
        }
    )
