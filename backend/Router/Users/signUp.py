from fastapi.responses import JSONResponse
import main
from Model import healthXUser


def signUp(requestedData):
    if healthXUser.readSingleUser(main.cursor, requestedData["userName"]) is not None:
        return JSONResponse(
            status_code=200,
            content={
                "detail": "User Name Already Exists"
            }
        )

    healthXUser.createUser(main.database, main.cursor, True, requestedData)

    return JSONResponse(
        status_code=200,
        content={
            "detail": "User Created SuccessFully"
        }
    )
