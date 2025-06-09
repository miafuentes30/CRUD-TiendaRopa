from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal
from datetime import date

class EstadoPedido(str, Enum):
    PENDIENTE = 'PENDIENTE'
    ENVIADO = 'ENVIADO'    
    ENTREGADO = 'ENTREGADO' 

class TallaRopa(str, Enum):
    XS = 'XS'
    S = 'S'
    M = 'M'
    L = 'L'
    XL = 'XL'
    XXL = 'XXL'

class ClienteBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    nombre: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., pattern=r'^[^@]+@[^@]+\.[^@]+$', max_length=100)  
    telefono: Optional[str] = Field(None, max_length=15)

class ClienteCreate(ClienteBase):
    pass

class Cliente(ClienteBase):
    id_cliente: int
    fecha_registro: date

class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=200)
    descripcion: str = Field(..., min_length=1)
    precio: float = Field(..., gt=0)
    talla: TallaRopa

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id_producto: int

class DetallePedidoBase(BaseModel):
    id_producto: int = Field(..., gt=0)
    cantidad: int = Field(..., gt=0)
    precio_unitario: float = Field(..., gt=0)

class PedidoBase(BaseModel):
    id_cliente: int
    estado: EstadoPedido = EstadoPedido.PENDIENTE
    detalles: List[DetallePedidoBase]

class PedidoCreate(PedidoBase):
    pass

class Pedido(PedidoBase):
    model_config = ConfigDict(from_attributes=True)
    
    id_pedido: int
    fecha_pedido: date

class VistaPedido(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id_pedido: int
    nombre_cliente: str
    fecha_pedido: str
    estado: str
    nombre_producto: str
    cantidad: int
    precio_unitario: float
    subtotal: float

class PedidoDetallado(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id_pedido: int
    fecha_pedido: str
    estado: EstadoPedido
    detalles: List[DetallePedidoBase]
    cliente: Cliente