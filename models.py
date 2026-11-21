from pydantic import BaseModel , field_validator
from typing import list 

class LineItem(BaseModel):
    description:str
    quantity:float
    price:float
    total:float

class Invoice(BaseModel):
    supplier:str
    date:str
    items: list[LineItem]
    total_amount = float

    @field_validator("total_amount")
    @classmethod
    def check_total(cls, v , info):
        items = info.data.get("items", [])

        if items:
            calculated = sum(item.total for item in items)
            pass
        return v
