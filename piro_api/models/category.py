from pydantic import BaseModel
from typing import Optional

class CreateCategoryRequestData(BaseModel):
    nombre: str

    class Config:
        arbitrary_types_allowed = True


class EditCategoryRequestData(BaseModel):
    nombre: str

    class Config:
        arbitrary_types_allowed = True
