from piro_api.orm import Venta, DetalleVenta
from sqlalchemy import func, or_, select, and_, insert, delete
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta

def get_reportes(session, limit: int, offset: int, filtro_tiempo=None):
    query = session.query(Venta)

    if filtro_tiempo == "Dia":
        # Filtrar por ventas del día actual
        today = datetime.now().date()
        query = query.filter(Venta.fecha >= today, Venta.fecha <= today + timedelta(days=1))
    elif filtro_tiempo == "Semana":
        # Filtrar por ventas de la semana actual
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=7)
        query = query.filter(Venta.fecha >= start_of_week, Venta.fecha < end_of_week)
    elif filtro_tiempo == "Mes":
        # Filtrar por ventas del mes actual
        today = datetime.now().date()
        start_of_month = today.replace(day=1)
        next_month = start_of_month.replace(month=start_of_month.month+1, day=1)
        query = query.filter(Venta.fecha >= start_of_month, Venta.fecha < next_month)
    elif filtro_tiempo == "TODO":
        # No aplicar filtro de tiempo, mostrar todos los registros
        pass

    query = (query.limit(limit).offset(offset).
             options(joinedload(Venta.detalles_venta).joinedload(DetalleVenta.producto)))

    products = query.all()


    return products


def make_product_table_from_register(register):
    detalles_venta = []

    # Suponiendo que 'detalles_venta' es la relación en el objeto 'Venta' que almacena los detalles
    for detalle in register.detalles_venta:
        detalles_venta.append({
            'idDetalleVenta': detalle.idDetalleVenta,
            'idVenta': detalle.idVenta,
            'cantidad': detalle.cantidad,
            'total_detalle': detalle.total_detalle,
            'idProducto': detalle.idProducto,
            'es_mayoreo': detalle.es_mayoreo,
            'fecha_detalle': detalle.fecha,
            'producto': {
                'idProducto': detalle.producto.idProducto,
                'nombre': detalle.producto.nombre,
                'precio_mayoreo': detalle.producto.precio_mayoreo,
                'stock_minimo': detalle.producto.stock_minimo,
                'is_active': detalle.producto.is_active,
                'precio_menudeo': detalle.producto.precio_menudeo,
                'stock': detalle.producto.stock,
                'categoria_id': detalle.producto.categoria_id
            }
        })



    return {
        'idVenta': register.idVenta,
        'total': register.total,
        'fecha': register.fecha,
        'detalles_venta': detalles_venta,
    }

def get_reportes_count(session, filtro_tiempo=None):
    print ("Que tiempo ", filtro_tiempo)
    query = session.query(func.count(Venta.idVenta))
    if filtro_tiempo == "Dia":
        print ("Entro")
        today = datetime.now().date()
        query = query.filter(Venta.fecha >= today, Venta.fecha <= today + timedelta(days=1))
    elif filtro_tiempo == "Semana":
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=7)
        query = query.filter(Venta.fecha >= start_of_week, Venta.fecha < end_of_week)
    elif filtro_tiempo == "Mes":
        print ("Holaaa")
        today = datetime.now().date()
        start_of_month = today.replace(day=1)
        next_month = start_of_month.replace(month=start_of_month.month + 1, day=1)
        query = query.filter(Venta.fecha >= start_of_month, Venta.fecha < next_month)
    elif filtro_tiempo == "Todo":
        # No aplicar filtro de tiempo, contar todos los registros
        pass
    count = query.scalar()
    return count

def get_reportes_total(session, filtro_tiempo=None):
    query = session.query(Venta)

    if filtro_tiempo == "Dia":
        # Filtrar por ventas del día actual
        today = datetime.now().date()
        query = query.filter(Venta.fecha >= today, Venta.fecha <= today + timedelta(days=1))
    elif filtro_tiempo == "Semana":
        # Filtrar por ventas de la semana actual
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=7)
        query = query.filter(Venta.fecha >= start_of_week, Venta.fecha < end_of_week)
    elif filtro_tiempo == "Mes":
        # Filtrar por ventas del mes actual
        today = datetime.now().date()
        start_of_month = today.replace(day=1)
        next_month = start_of_month.replace(month=start_of_month.month+1, day=1)
        query = query.filter(Venta.fecha >= start_of_month, Venta.fecha < next_month)
    elif filtro_tiempo == "TODO":
        # No aplicar filtro de tiempo, mostrar todos los registros
        pass

    query = (query.options(joinedload(Venta.detalles_venta).joinedload(DetalleVenta.producto)))

    products = query.all()
    total_ventas = sum(product.total for product in products)
    return total_ventas