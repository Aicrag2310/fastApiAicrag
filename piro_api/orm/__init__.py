from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'Productos'

    idProducto = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)
    precio_menudeo = Column(Float, nullable=False)
    precio_mayoreo = Column(Float)
    stock = Column(Integer, nullable=False)
    stock_minimo = Column(Integer)
    categoria_id = Column(Integer, ForeignKey('Categorias.id'), nullable=False)  # Agrega ForeignKey
    is_active = Column(Boolean, default=True)
    categoria = relationship("Categoria")  # Establece la relación

class Categoria(Base):
    __tablename__ = 'Categorias'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)

class Venta(Base):
    __tablename__ = 'Ventas'

    idVenta = Column(Integer, primary_key=True)
    total = Column(Float)
    fecha = Column(DateTime)
    detalles_venta = relationship("DetalleVenta", back_populates="venta")

class DetalleVenta(Base):
    __tablename__ = 'DetallesVenta'

    idDetalleVenta = Column(Integer, primary_key=True)
    idVenta = Column(Integer, ForeignKey('Ventas.idVenta'))
    idProducto = Column(Integer, ForeignKey('Productos.idProducto'))
    cantidad = Column(Integer)
    es_mayoreo = Column(Boolean, nullable=True)
    total_detalle = Column(Float)
    fecha = Column(DateTime)
    venta = relationship("Venta", back_populates="detalles_venta")
    producto = relationship("Product")
