from pydantic import BaseModel
from typing import Optional

class CreateProductRequestData(BaseModel):
    nombre: str
    precio_menudeo: float
    precio_mayoreo: Optional[float]
    stock: int
    stock_minimo: Optional[int]
    categoria_id: Optional[int]
    is_active: Optional[bool] = True

    class Config:
        arbitrary_types_allowed = True


class EditProductRequestData(BaseModel):
    nombre: str
    precio_menudeo: int
    precio_mayoreo: Optional[int]
    stock: int
    stock_minimo: Optional[int]
    categoria_id: Optional[int]
    is_active: Optional[bool] = True

    class Config:
        arbitrary_types_allowed = True
