from fastapi.responses import JSONResponse
from Controller import JWTCheck
from Model import healthXUserCRUD
import main


def createData(requestedData, requestedHeader):
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

    healthXUserCRUD.createSingleUserTask(
        main.database, main.cursor, userName, True, requestedData)

    return JSONResponse(
        status_code=200,
        content={
            "detail": "Created Successfully"
        }
    )
