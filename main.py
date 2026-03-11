import json
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

import uvicorn

#ggg

app = FastAPI()
#DB_FILE = "./database.json"


@app.get("/")
async def read_main():
    return {"msg": "Hello World Python fastapi"}

if __name__ == "__main__":
    # Azure จะกำหนดพอร์ตให้ผ่านตัวแปร "PORT"
    port = int(os.environ.get("PORT", 8000)) 
    uvicorn.run("main:app", host="0.0.0.0", port=port)

