from Model import healthXUser
from fastapi import Request, HTTPException


def verify(cursor):
    async def checker(request: Request):
        requestedData = await request.json()

        if healthXUser.readSingleUser_Password(cursor, requestedData) is None:
            raise HTTPException(status_code=401, detail="Unauthorized , User or Password Invalid")

    return checker