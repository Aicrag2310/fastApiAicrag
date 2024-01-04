import bcrypt
import csv
import io
import re
from piro_api.orm import Categoria
from sqlalchemy import func, or_, select, and_, insert, delete


def get_products_category_data(session, limit: int, offset: int, search_query=None):
    query = session.query(Categoria)


    if search_query:
        # Divide la consulta de búsqueda en palabras individuales
        search_words = search_query.split()

        # Crea listas de declaraciones para cada palabra en la consulta de búsqueda
        nombre_stmts = []
        for word in search_words:
            nombre_stmts.append(Categoria.nombre.like(f'%{word}%'))

        # Combina las declaraciones 'like' utilizando el operador 'or_' en cada campo de consulta
        query = query.filter(
            or_(
                and_(*nombre_stmts)
            )
        )

    query = query.limit(limit).offset(offset)

    return query.all()

def make_category_table_from_register(register: Categoria):
    return {
        'id': register.id,
        'name': register.nombre,
    }

def get_category_catalog_count(session, search_query):
    query = session.query(func.count(Categoria.id))

    if search_query:
        # Divide la consulta de búsqueda en palabras individuales
        search_words = search_query.split()

        # Crea listas de declaraciones para cada palabra en la consulta de búsqueda
        nombre_stmts = []
        # Modifica los nombres de las columnas según corresponda a tu tabla
        for word in search_words:
            nombre_stmts.append(Categoria.nombre.like(f'%{word}%'))

        # Combina las declaraciones 'like' utilizando el operador 'or_' en cada campo de consulta
        query = query.filter(
            or_(
                and_(*nombre_stmts),
            )
        )

    count = query.scalar()
    return count