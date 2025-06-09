from sqlalchemy.orm import Session
from models import Cliente, Producto, Pedido, DetallePedido
from typing import List, Optional
from sqlalchemy import text

# CRUD para Clientes
def crear_cliente(db: Session, nombre: str, email: str, telefono: Optional[str] = None):
    db_cliente = Cliente(nombre=nombre, email=email, telefono=telefono)
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def obtener_clientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Cliente).offset(skip).limit(limit).all()

def obtener_cliente(db: Session, cliente_id: int):
    return db.query(Cliente).filter(Cliente.id_cliente == cliente_id).first()

def obtener_cliente_por_email(db: Session, email: str):
    """Función para obtener cliente por email - evita duplicados"""
    return db.query(Cliente).filter(Cliente.email == email).first()

def actualizar_cliente(db: Session, cliente_id: int, nombre: str, email: str, telefono: Optional[str] = None):
    cliente = db.query(Cliente).filter(Cliente.id_cliente == cliente_id).first()
    if cliente:
        cliente.nombre = nombre
        cliente.email = email
        cliente.telefono = telefono
        db.commit()
        db.refresh(cliente)
    return cliente

def eliminar_cliente(db: Session, cliente_id: int):
    cliente = db.query(Cliente).filter(Cliente.id_cliente == cliente_id).first()
    if cliente:
        db.delete(cliente)
        db.commit()
    return cliente

# CRUD para Productos
def crear_producto(db: Session, nombre: str, descripcion: str, precio: float, talla: str):
    db_producto = Producto(nombre=nombre, descripcion=descripcion, precio=precio, talla=talla)
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def obtener_productos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Producto).offset(skip).limit(limit).all()

def obtener_producto(db: Session, producto_id: int):
    return db.query(Producto).filter(Producto.id_producto == producto_id).first()

def actualizar_producto(db: Session, producto_id: int, nombre: str, descripcion: str, precio: float, talla: str):
    producto = db.query(Producto).filter(Producto.id_producto == producto_id).first()
    if producto:
        producto.nombre = nombre
        producto.descripcion = descripcion
        producto.precio = precio
        producto.talla = talla
        db.commit()
        db.refresh(producto)
    return producto

def eliminar_producto(db: Session, producto_id: int):
    producto = db.query(Producto).filter(Producto.id_producto == producto_id).first()
    if producto:
        db.delete(producto)
        db.commit()
    return producto

# CRUD para Pedidos con Detalles
def crear_pedido(db: Session, id_cliente: int, estado: str, detalles: List[dict]):
    try:
        db_pedido = Pedido(id_cliente=id_cliente, estado=estado)
        db.add(db_pedido)
        db.commit()
        db.refresh(db_pedido)
        
        for detalle in detalles:
            db_detalle = DetallePedido(
                id_pedido=db_pedido.id_pedido,
                id_producto=detalle['id_producto'],
                cantidad=detalle['cantidad'],
                precio_unitario=detalle['precio_unitario']
            )
            db.add(db_detalle)
        
        db.commit()
        db.refresh(db_pedido)
        return db_pedido
    except Exception as e:
        db.rollback()
        raise e

def obtener_pedidos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Pedido).offset(skip).limit(limit).all()

def obtener_pedido(db: Session, pedido_id: int):
    return db.query(Pedido).filter(Pedido.id_pedido == pedido_id).first()

def actualizar_pedido(db: Session, pedido_id: int, estado: str, detalles: List[dict]):
    try:
        pedido = db.query(Pedido).filter(Pedido.id_pedido == pedido_id).first()
        if pedido:
            pedido.estado = estado
            
            # Eliminar detalles existentes
            db.query(DetallePedido).filter(DetallePedido.id_pedido == pedido_id).delete()
            
            # Agregar nuevos detalles
            for detalle in detalles:
                db_detalle = DetallePedido(
                    id_pedido=pedido_id,
                    id_producto=detalle['id_producto'],
                    cantidad=detalle['cantidad'],
                    precio_unitario=detalle['precio_unitario']
                )
                db.add(db_detalle)
            
            db.commit()
            db.refresh(pedido)
        return pedido
    except Exception as e:
        db.rollback()
        raise e

def eliminar_pedido(db: Session, pedido_id: int):
    try:
        pedido = db.query(Pedido).filter(Pedido.id_pedido == pedido_id).first()
        if pedido:
            db.delete(pedido)
            db.commit()
        return pedido
    except Exception as e:
        db.rollback()
        raise e

# Vista para mostrar información combinada
def obtener_vista_pedidos(db: Session):
    try:
        result = db.execute(text("SELECT * FROM vista_pedidos_completos"))
        return [{
            **dict(row._mapping),
            'fecha_pedido': str(row._mapping['fecha_pedido'])  # Convert date to string
        } for row in result]
    except Exception as e:
        raise e