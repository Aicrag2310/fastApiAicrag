import bcrypt
import csv
import io
import re
from piro_api.orm import Product, Categoria
from sqlalchemy import func, or_, select, and_, insert, delete
from sqlalchemy.orm import joinedload


def get_products_catalog_data(session, limit: int, offset: int, search_query=None):
    query = session.query(Product)

    query = query.filter(Product.is_active == 1)

    if search_query:
        # Divide la consulta de búsqueda en palabras individuales
        search_words = search_query.split()

        # Crea listas de declaraciones para cada palabra en la consulta de búsqueda
        nombre_stmts = []
        for word in search_words:
            nombre_stmts.append(Product.nombre.like(f'%{word}%'))

        # Combina las declaraciones 'like' utilizando el operador 'or_' en cada campo de consulta
        query = query.filter(or_(*nombre_stmts))

    query = query.limit(limit).offset(offset).options(joinedload(Product.categoria))  # Carga la relación Categoria

    products = query.all()

    # Lista para almacenar los resultados con información de categoría
    products_with_category = []

    for product in products:
        # Obtén el nombre de la categoría desde la relación establecida
        category_name = product.categoria.nombre if product.categoria else None

        # Crea un diccionario con la información del producto y su categoría
        product_with_category = {
            "idProducto": product.idProducto,
            "nombre": product.nombre,
            "precio_mayoreo": product.precio_mayoreo,
            "precio_menudeo": product.precio_menudeo,
            "stock": product.stock,
            "categoria_nombre": category_name,  # Agrega el nombre de la categoría al diccionario
            "stock_minimo": product.stock_minimo,
            "is_active": product.is_active
        }

        # Agrega el diccionario a la lista de productos con información de categoría
        products_with_category.append(product_with_category)

    return products_with_category

def make_product_table_from_register(register):
    return {
        'id': register['idProducto'],
        'name': register['nombre'],
        'precio_menudeo': register['precio_menudeo'],
        'precio_mayoreo': register['precio_mayoreo'],
        'stock': register['stock'],
        'stock_minimo': register['stock_minimo'],
        'categoria': register['categoria_nombre'],  # Ajusta la clave según corresponda
        'is_active': register['is_active'],
    }


def get_products_catalog_count(session, search_query):
    query = session.query(func.count(Product.idProducto))
    query = query.filter(Product.is_active == True)  # Cambia 1 por True para una columna booleana

    if search_query:
        # Divide la consulta de búsqueda en palabras individuales
        search_words = search_query.split()

        # Crea listas de declaraciones para cada palabra en la consulta de búsqueda
        nombre_stmts = []
        # Modifica los nombres de las columnas según corresponda a tu tabla
        for word in search_words:
            nombre_stmts.append(Product.nombre.like(f'%{word}%'))

        # Combina las declaraciones 'like' utilizando el operador 'or_' en cada campo de consulta
        query = query.filter(
            or_(
                and_(*nombre_stmts),
            )
        )

    count = query.scalar()
    return count