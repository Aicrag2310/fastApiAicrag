from fastapi import APIRouter, Header, Depends, HTTPException
from sqlalchemy.orm import Session
from piro_api.database import get_db
from piro_api.models.ventas import CreateVentaRequestData
import piro_api.processes.ventas as processes

router = APIRouter()

@router.post('/api/venta')
def create_venta(request_data: CreateVentaRequestData,
                 accept_language: str = Header(default='en'),
                 db: Session = Depends(get_db)):

    try:
        guardar_venta = processes.saveVenta(db, request_data.totalCompleto)

        for product in request_data.productos:
            validate = processes.validateQuantity(db, product.id, product.quantity)
            if not validate:
                raise HTTPException(status_code=400, detail='Error: cantidad insuficiente para un producto')
            guardar_detalle_venta = processes.saveDetalleVenta(db, product, guardar_venta)
        total_completo = request_data.totalCompleto
        # Realizar operaciones con el total completo

        return {"message": "Venta creada exitosamente"}  # Retorna un mensaje de éxito

    except HTTPException as e:
        # Si hay una excepción de tipo HTTPException, se maneja aquí
        return {"error": e.detail}  # Retorna el detalle del error

    except Exception as e:
        # Si ocurre un error inesperado, lo manejas aquí
        return {"error": "Ocurrió un error en el servidor"}  # Retorna un mensaje de error genérico
