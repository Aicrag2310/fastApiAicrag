from pydantic import BaseModel
from datetime import datetime


class AppGenericException(Exception):
    def __init__(self, code: int, message: str, http_response_status_code: int = None):
        self.code = code
        self.message = message
        self.http_response_status_code = http_response_status_code


class MessageResponse(BaseModel):
    message: str
    code: int

