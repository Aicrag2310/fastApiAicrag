from fastapi import APIRouter, Header, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from piro_api.database import get_db
from datetime import datetime, timedelta
from piro_api.orm import Venta, DetalleVenta
import piro_api.processes.reportes as processes



router = APIRouter()

@router.get('/api/reporte/data')
def get_table_data(limit: int = 10,
                   offset: int = 0,
                   reporte: str = '',
                   accept_language: str = Header(default='en'),
                   db: Session = Depends(get_db)):
    registers = processes.get_reportes(db, limit, offset, reporte)
    data = [processes.make_product_table_from_register(register) for register in registers]

    return data

@router.get('/api/reporte/count')
def get_table_count(reporte: str = '',
                    accept_language: str = Header(default='en'),
                    db: Session = Depends(get_db)):
    return {'count': processes.get_reportes_count(db, reporte)}

@router.get('/api/reporte/total')
def get_table_count(reporte: str = '',
                    accept_language: str = Header(default='en'),
                    db: Session = Depends(get_db)):
    return {'Total  ': processes.get_reportes_total(db, reporte)}



