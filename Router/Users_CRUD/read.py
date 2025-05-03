from fastapi.responses import JSONResponse
from Controller import JWTCheck
from Model import healthXUserCRUD
import main

def readData(requestedHeader):
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
    data = healthXUserCRUD.readAllSingleUserTask(main.cursor, userName)
    columns = [columnsDescription[0] for columnsDescription in main.cursor.description]
    results = []

    for rows in data:
        results.append(dict(zip(columns, rows)))

    return JSONResponse(
        status_code=200,
        content={
            "detail": "Readed Successfully",
            "data": results
        }
    )
