from typing import Optional, List

from pydantic import BaseModel


class AuthRequest(BaseModel):
    username: str
    password: str


class UserClaims(BaseModel):
    employee_id: int = 0
    username: str
    firstname: str
    lastname: str
    store: Optional[List[int]] = [1]
