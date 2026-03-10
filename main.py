import json
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional





app = FastAPI()
DB_FILE = "./database.json"




# Data Model
class Item(BaseModel):
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

@app.get("/items", response_model=List[Item])
def get_items():
    return read_db()

@app.post("/items", response_model=Item)
def create_item(item: Item):
    db = read_db()
    if any(i['id'] == item.id for i in db):
        raise HTTPException(status_code=400, detail="ID already exists")
    db.append(item.dict())
    write_db(db)
    return item

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    db = read_db()
    for index, item in enumerate(db):
        if item['id'] == item_id:
            db[index] = updated_item.dict()
            write_db(db)
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    db = read_db()
    new_db = [i for i in db if i['id'] != item_id]
    if len(new_db) == len(db):
        raise HTTPException(status_code=404, detail="Item not found")
    write_db(new_db)
    return {"message": "Item deleted successfully"}