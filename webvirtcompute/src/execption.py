import json
from fastapi import HTTPException


def raise_error_msg(msg):
    raise HTTPException(status_code=400, detail=str(msg))
