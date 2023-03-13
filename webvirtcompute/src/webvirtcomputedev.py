#!/usr/bin/env python3

import os
import uvicorn
from settings import HOST, PORT


if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True, access_log=False)
