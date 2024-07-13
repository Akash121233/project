from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

# Load data from CSV
dat = pd.read_csv("data.csv")
df = pd.DataFrame(dat)
a = df.to_numpy()

app = FastAPI()

class Item(BaseModel):
    SI_no: int
    Item_name: str
    Rate: float
    Quantity_Available: int

class PurchaseItem(BaseModel):
    Item_name: str
    Quantity: int

class PurchaseRequest(BaseModel):
    items: list[PurchaseItem]

@app.get("/items/{item_name}", response_model=Item)
def get_item(item_name: str):
    for row in a:
        if row[1] == item_name:
            return Item(SI_no=row[0], Item_name=row[1], Rate=row[3], Quantity_Available=row[2])
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/purchase")
def purchase_items(purchase_request: PurchaseRequest):
    total_bill = 0

    for purchase_item in purchase_request.items:
        item_name = purchase_item.Item_name
        quantity = purchase_item.Quantity
        item_data = None

        for row in a:
            if row[1] == item_name:
                item_data = row
                break

        if item_data is None:
            raise HTTPException(status_code=404, detail=f"Item {item_name} not found")

        available_quantity = item_data[2]
        rate = item_data[3]

        if quantity > available_quantity:
            raise HTTPException(status_code=400, detail=f"Not enough {item_name} in stock")

        total_bill += quantity * rate
        item_data[2] -= quantity

    return {"total_bill": total_bill}

@app.get("/items", response_model=list[Item])
def get_all_items():
    items = []
    for row in a:
        items.append(Item(SI_no=row[0], Item_name=row[1], Rate=row[3], Quantity_Available=row[2]))
    return items

# To run the FastAPI server, use the command:
# uvicorn app:app --reload
