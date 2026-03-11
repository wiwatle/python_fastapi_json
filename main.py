import json
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

import uvicorn

#ggg

app = FastAPI()
DB_FILE = "./database.json"


@app.get("/")
async def read_main():
    return {"msg": "Hello World Python fastapi"}

if __name__ == "__main__":
    # Azure จะกำหนดพอร์ตให้ผ่านตัวแปร "PORT"
    port = int(os.environ.get("PORT", 8000)) 
    uvicorn.run("main:app", host="0.0.0.0", port=port)



# Data Model
class Products(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float

# Helper functions to handle JSON I/O
def read_db():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)

def write_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- Routes ---

@app.get("/products", response_model=List[Products])
def get_items():
    return read_db()

@app.post("/products", response_model=Products)
def create_item(item: Products):
    db = read_db()
    if any(i['id'] == item.id for i in db):
        raise HTTPException(status_code=400, detail="ID already exists")
    db.append(item.dict())
    write_db(db)
    return item

@app.put("/products/{item_id}", response_model=Products)
def update_item(item_id: int, updated_item: Products):
    db = read_db()
    for index, item in enumerate(db):
        if item['id'] == item_id:
            db[index] = updated_item.dict()
            write_db(db)
            return updated_item
    raise HTTPException(status_code=404, detail="Products not found")

@app.delete("/products/{item_id}")
def delete_item(item_id: int):
    db = read_db()
    new_db = [i for i in db if i['id'] != item_id]
    if len(new_db) == len(db):
        raise HTTPException(status_code=404, detail="Products not found")
    write_db(new_db)
    return {"message": "Products deleted successfully"}