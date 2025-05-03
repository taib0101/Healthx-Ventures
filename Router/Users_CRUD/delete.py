from fastapi.responses import JSONResponse
from Controller import JWTCheck
from Model import healthXUserCRUD
import main

def deleteData(requestedHeader):
    token = requestedHeader["token"]
    checkJWT = JWTCheck.check_jwt_expiry(token)

    if checkJWT["valid"] is False:
        return JSONResponse(
            status_code=401,
            content={
                "detail": "Expire or Invalid Token"
            }
        )

    taskId = requestedHeader["id"]
    healthXUserCRUD.deleteSingleUserTask(main.database, main.cursor, taskId)

    return JSONResponse(
        status_code=200,
        content={
            "detail": "Deleted Successfully"
        }
    )
