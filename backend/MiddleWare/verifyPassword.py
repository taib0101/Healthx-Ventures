from Model import healthXUser

def verify(cursor, requestedData):
    readUserPassword = healthXUser.readSingleUser_Password(cursor, requestedData)

    if readUserPassword is None:
        return False
    
    return True