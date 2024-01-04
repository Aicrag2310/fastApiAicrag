import logging
import pathlib
import uuid
from datetime import datetime
from fastapi import APIRouter, Header, Depends, UploadFile, File
from sqlalchemy.orm import Session
from starlette.responses import FileResponse, StreamingResponse
from typing import List, Optional
from piro_api.database import get_db
import piro_api.processes.category as processes
from piro_api.models.category import CreateCategoryRequestData, EditCategoryRequestData
from piro_api import get_settings, AppGenericException
from piro_api.orm import Categoria

router = APIRouter()

@router.get('/api/category/table/data')
def get_table_data(limit: int = 10,
                   offset: int = 0,
                   query: str = '',
                   accept_language: str = Header(default='en'),
                   db: Session = Depends(get_db)):
    registers = processes.get_products_category_data(db, limit, offset, query)
    data = [processes.make_category_table_from_register(register) for register in registers]

    return data

@router.get('/api/category/table/count')
def get_table_count(query: str = '',
                    accept_language: str = Header(default='en'),
                    db: Session = Depends(get_db)):
    return {'count': processes.get_category_catalog_count(db, query)}



@router.post('/api/category')
def create_product(request_data: CreateCategoryRequestData,
                   accept_language: str = Header(default='en'),
                   db: Session = Depends(get_db)):
    config = get_settings()
    try:
        categoria = Categoria()
        categoria.nombre = request_data.nombre

        db.add(categoria)
        db.commit()

        return {'id': categoria.id, 'message': 'Category created'}
    except Exception as e:
        print(e)
        raise AppGenericException(0, 'Error creating Category', 400)


@router.put('/api/category/{product_id}')
def edit_product(product_id: int,
                 request_data: EditCategoryRequestData,
                 accept_language: str = Header(default='en'),
                 db: Session = Depends(get_db)):
    try:
        register: Categoria = db.query(Categoria).get(product_id)

        register.nombre = request_data.nombre


        db.commit()

        return {'message': 'Updated register'}
    except Exception as e:
        raise AppGenericException(0, f'Category can not be updated. {e}', 400)


@router.delete('/api/category/{category_id}')
def delete_product(category_id: int,
                   db: Session = Depends(get_db)):
    try:
        category = db.query(Categoria).filter(Categoria.id == category_id).first()
        if category:
            # Si se encontró la categoría, la eliminamos
            db.delete(category)
            db.commit()
            return {'message': 'Categoría eliminada'}
        else:
            return {'message': 'Categoría no encontrada'}
    except Exception as e:
        return {'message': 'Error al eliminar el producto', 'error': str(e)}
