from fastapi import APIRouter, Header, Depends, HTTPException
from sqlalchemy.orm import Session
from piro_api.database import get_db
from piro_api.models.catalogs import UserFormRequestData
import piro_api.processes.catalogs as processes

router = APIRouter()

@router.post('/api/user')
def create_register(request_data: UserFormRequestData,
                    accept_language: str = Header(default='en'),
                    db: Session = Depends(get_db)):
    processes.validate_user_form_request_data(db, None, request_data)
    new_register = processes.create_user_from_request_data(db, request_data)

    return {'message': 'Register created successfully', 'id': new_register.id}