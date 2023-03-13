from secrets import compare_digest
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from settings import TOKEN

security = HTTPBasic()
token = TOKEN


def basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = compare_digest(credentials.username, token)
    correct_password = compare_digest(credentials.password, token)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Basic"},
        )
    return token
