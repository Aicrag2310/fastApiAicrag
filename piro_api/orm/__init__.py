from sqlalchemy import Table, create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey, TIMESTAMP, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from typing import Final, List, Optional


Base = declarative_base()   

user_role = Table('UserRole',
                  Base.metadata,
                  Column('id', Integer, primary_key=True),
                  Column('roleId', Integer, ForeignKey('Role.id'), nullable=True),
                  Column('userId', Integer, ForeignKey('User.id'), nullable=True)
                  )

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


class User(Base):
    __tablename__ = 'User'
    __table_args__ = (
        UniqueConstraint('username'),
        UniqueConstraint('phone_number'),
        UniqueConstraint('email'),
    )

    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(String(100))
    firstname = Column(String(50))
    lastname = Column(String(50))
    isactive = Column(Boolean)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)
    phone_number = Column(String(20))
    email = Column(String(100))

    roles = relationship('Role', secondary=user_role, back_populates='users')

    #roles: List['Role'] = relationship('Role', secondary=user_role, back_populates='users')

    



    def __repr__(self):
        return f"<User(username='{self.username}', firstname='{self.firstname}', lastname='{self.lastname}')>"
    

class Role(Base):
    __tablename__ = 'Role'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    isActive = Column(Integer, nullable=True)

    users = relationship('User', secondary=user_role, back_populates='roles')

    #users: List[User] = relationship('User', secondary=user_role, back_populates='roles')

    def __repr__(self) -> str:
        return '<Role [id={}] [name={}]>'.format(self.id, self.name)
    
class Attribute(Base):
    __tablename__ = 'Attribute'
    __table_args__ = (
        Index('ix_Attribute_code', 'code'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    code = Column(String(100), nullable=False)
    isActive = Column(Integer, nullable=True)

    def __repr__(self) -> str:
        return '<Attribute [id={}]>'.format(self.id)
    
    
class RoleAttribute(Base):
    __tablename__ = 'RoleAttribute'

    id = Column(Integer, primary_key=True)
    roleId = Column(Integer, ForeignKey('Role.id'), nullable=True)
    attributeId = Column(Integer, ForeignKey('Attribute.id'), nullable=True)

    def __repr__(self) -> str:
        return '<RoleAttribute [id={}]>'.format(self.id)