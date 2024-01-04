from pydantic import BaseModel
from typing import List

class ProductItem(BaseModel):
    id: int
    name: str
    quantity: int
    subtotal: float
    totalPorProducto: float

class CreateVentaRequestData(BaseModel):
    productos: List[ProductItem]
    totalCompleto: float

    class Config:
        arbitrary_types_allowed = True
