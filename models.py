from sqlalchemy import Column, Integer, String, Date, Enum, Numeric, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base
from enum import Enum as PyEnum

# Enums para tipos personalizados 
class EstadoPedido(PyEnum):
    PENDIENTE = 'PENDIENTE' 
    ENVIADO = 'ENVIADO'       
    ENTREGADO = 'ENTREGADO'  

class TallaRopa(PyEnum):
    XS = 'XS'
    S = 'S'
    M = 'M'
    L = 'L'
    XL = 'XL'
    XXL = 'XXL'

#  Cliente
class Cliente(Base):
    __tablename__ = 'clientes'

    id_cliente = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telefono = Column(String(15))
    fecha_registro = Column(Date, server_default='CURRENT_DATE')
    
    pedidos = relationship("Pedido", back_populates="cliente", cascade="all, delete")

# Producto
class Producto(Base):
    __tablename__ = 'productos'

    id_producto = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(String)
    precio = Column(Numeric(10, 2), nullable=False)
    talla = Column(Enum(TallaRopa))
    
    detalles_pedido = relationship("DetallePedido", back_populates="producto")

# Pedido
class Pedido(Base):
    __tablename__ = 'pedidos'

    id_pedido = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente', ondelete='CASCADE'))
    fecha_pedido = Column(Date, server_default='CURRENT_DATE')
    estado = Column(Enum(EstadoPedido), nullable=False, server_default='PENDIENTE')  # Cambiado default
    
    cliente = relationship("Cliente", back_populates="pedidos")
    detalles = relationship("DetallePedido", back_populates="pedido", cascade="all, delete")

# DetallePedido (tabla intermedia)
class DetallePedido(Base):
    __tablename__ = 'detalle_pedidos'

    id_detalle = Column(Integer, primary_key=True, index=True)
    id_pedido = Column(Integer, ForeignKey('pedidos.id_pedido', ondelete='CASCADE'))
    id_producto = Column(Integer, ForeignKey('productos.id_producto', ondelete='CASCADE'))
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    
    pedido = relationship("Pedido", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles_pedido")