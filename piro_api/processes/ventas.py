import bcrypt
import csv
import io
import re
from datetime import datetime
from piro_api.orm import Product, Venta, DetalleVenta
from sqlalchemy import func, or_, select, and_, insert, delete
from piro_api import get_settings, AppGenericException

def validateQuantity(session, product_id, quantity):
    product = (
        session.query(Product)
        .filter(Product.idProducto == product_id)
        .first()
    )

    if product:
        if product.stock >= quantity:
            return True, f"La cantidad solicitada ({quantity}) es válida para el producto '{product.nombre}'"
        else:
            return False
    else:
        return False, f"No se encontró un producto con el ID '{product_id}'"

def saveVenta(session, total):
    venta = Venta(total=total, fecha=datetime.now())

    session.add(venta)
    session.commit()

    return venta.idVenta  # Retorna el ID de la venta recién creada


def saveDetalleVenta (session, producto, guardar_venta):
    id = producto.id
    idventa = guardar_venta

    quantity = producto.quantity

    subtotal = producto.subtotal
    total = producto.totalPorProducto
    try:
        detailVentas = DetalleVenta()
        detailVentas.idVenta = idventa
        detailVentas.idProducto = id
        detailVentas.cantidad = quantity
        detailVentas.total_detalle = total
        detailVentas.fecha = datetime.now()
        session.add(detailVentas)
        session.commit()
    except Exception as e:
        print(e)
        raise AppGenericException(0, 'Error creating details Venta', 400)


