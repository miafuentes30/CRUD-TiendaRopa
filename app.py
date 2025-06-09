from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
import crud
import models
import schemas
from database import SessionLocal, engine, get_db

# Crear las tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Tienda de Ropa", version="1.0.0")

# CRUD para Clientes
@app.post("/clientes/", response_model=schemas.Cliente, status_code=status.HTTP_201_CREATED)
def crear_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    try:
        # Verificar si el email ya existe
        db_cliente = crud.obtener_cliente_por_email(db, email=cliente.email)
        if db_cliente:
            raise HTTPException(
                status_code=400, 
                detail=f"El email {cliente.email} ya está registrado"
            )
        
        return crud.crear_cliente(
            db=db, 
            nombre=cliente.nombre, 
            email=cliente.email, 
            telefono=cliente.telefono
        )
    except IntegrityError as e:
        db.rollback()
        if "clientes_email_key" in str(e):
            raise HTTPException(
                status_code=400, 
                detail=f"El email {cliente.email} ya está registrado"
            )
        else:
            raise HTTPException(status_code=400, detail="Error de integridad en la base de datos")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@app.get("/clientes/", response_model=List[schemas.Cliente])
def obtener_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        clientes = crud.obtener_clientes(db, skip=skip, limit=limit)
        return clientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener clientes: {str(e)}")

@app.get("/clientes/{cliente_id}", response_model=schemas.Cliente)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    try:
        db_cliente = crud.obtener_cliente(db, cliente_id=cliente_id)
        if db_cliente is None:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return db_cliente
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener cliente: {str(e)}")

@app.put("/clientes/{cliente_id}", response_model=schemas.Cliente)
def actualizar_cliente(cliente_id: int, cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    try:
        # Verificar si el cliente existe
        db_cliente = crud.obtener_cliente(db, cliente_id=cliente_id)
        if not db_cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
        # Verificar si el email ya existe en otro cliente
        cliente_email = crud.obtener_cliente_por_email(db, email=cliente.email)
        if cliente_email and cliente_email.id_cliente != cliente_id:
            raise HTTPException(
                status_code=400, 
                detail=f"El email {cliente.email} ya está registrado por otro cliente"
            )
        
        return crud.actualizar_cliente(
            db=db, 
            cliente_id=cliente_id, 
            nombre=cliente.nombre, 
            email=cliente.email, 
            telefono=cliente.telefono
        )
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        if "clientes_email_key" in str(e):
            raise HTTPException(
                status_code=400, 
                detail=f"El email {cliente.email} ya está registrado"
            )
        else:
            raise HTTPException(status_code=400, detail="Error de integridad en la base de datos")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar cliente: {str(e)}")

@app.delete("/clientes/{cliente_id}")
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    try:
        db_cliente = crud.eliminar_cliente(db, cliente_id=cliente_id)
        if db_cliente is None:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return {"mensaje": "Cliente eliminado exitosamente"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar cliente: {str(e)}")

# CRUD para Productos
@app.post("/productos/", response_model=schemas.Producto, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    try:
        return crud.crear_producto(
            db=db, 
            nombre=producto.nombre, 
            descripcion=producto.descripcion, 
            precio=producto.precio, 
            talla=producto.talla.value
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear producto: {str(e)}")

@app.get("/productos/", response_model=List[schemas.Producto])
def obtener_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        productos = crud.obtener_productos(db, skip=skip, limit=limit)
        return productos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener productos: {str(e)}")

@app.get("/productos/{producto_id}", response_model=schemas.Producto)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    try:
        db_producto = crud.obtener_producto(db, producto_id=producto_id)
        if db_producto is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return db_producto
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener producto: {str(e)}")

@app.put("/productos/{producto_id}", response_model=schemas.Producto)
def actualizar_producto(producto_id: int, producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    try:
        db_producto = crud.actualizar_producto(
            db=db, 
            producto_id=producto_id, 
            nombre=producto.nombre, 
            descripcion=producto.descripcion, 
            precio=producto.precio, 
            talla=producto.talla.value
        )
        if db_producto is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return db_producto
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar producto: {str(e)}")

@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    try:
        db_producto = crud.eliminar_producto(db, producto_id=producto_id)
        if db_producto is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return {"mensaje": "Producto eliminado exitosamente"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar producto: {str(e)}")

# CRUD para Pedidos
@app.post("/pedidos/", response_model=schemas.Pedido, status_code=status.HTTP_201_CREATED)
def crear_pedido(pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    try:
        # Verificar que el cliente existe
        cliente = crud.obtener_cliente(db, cliente_id=pedido.id_cliente)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
        # Verificar que todos los productos existen
        for detalle in pedido.detalles:
            producto = crud.obtener_producto(db, producto_id=detalle.id_producto)
            if not producto:
                raise HTTPException(
                    status_code=404, 
                    detail=f"Producto con ID {detalle.id_producto} no encontrado"
                )
        
        detalles_dict = [detalle.dict() for detalle in pedido.detalles]
        
        return crud.crear_pedido(
            db=db, 
            id_cliente=pedido.id_cliente, 
            estado=pedido.estado.value, 
            detalles=detalles_dict
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear pedido: {str(e)}")

@app.get("/pedidos/", response_model=List[schemas.Pedido])
def obtener_pedidos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        pedidos = crud.obtener_pedidos(db, skip=skip, limit=limit)
        return pedidos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener pedidos: {str(e)}")

@app.get("/pedidos/{pedido_id}", response_model=schemas.Pedido)
def obtener_pedido(pedido_id: int, db: Session = Depends(get_db)):
    try:
        db_pedido = crud.obtener_pedido(db, pedido_id=pedido_id)
        if db_pedido is None:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        return db_pedido
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener pedido: {str(e)}")

@app.put("/pedidos/{pedido_id}", response_model=schemas.Pedido)
def actualizar_pedido(pedido_id: int, pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    try:
        # Verificar que el pedido existe
        db_pedido = crud.obtener_pedido(db, pedido_id=pedido_id)
        if not db_pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        
        # Verificar que el cliente existe
        cliente = crud.obtener_cliente(db, cliente_id=pedido.id_cliente)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
        # Verificar que todos los productos existen
        for detalle in pedido.detalles:
            producto = crud.obtener_producto(db, producto_id=detalle.id_producto)
            if not producto:
                raise HTTPException(
                    status_code=404, 
                    detail=f"Producto con ID {detalle.id_producto} no encontrado"
                )
        
        detalles_dict = [detalle.dict() for detalle in pedido.detalles]
        
        return crud.actualizar_pedido(
            db=db, 
            pedido_id=pedido_id, 
            estado=pedido.estado.value, 
            detalles=detalles_dict
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar pedido: {str(e)}")

@app.delete("/pedidos/{pedido_id}")
def eliminar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    try:
        db_pedido = crud.eliminar_pedido(db, pedido_id=pedido_id)
        if db_pedido is None:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        return {"mensaje": "Pedido eliminado exitosamente"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar pedido: {str(e)}")

# Vista de pedidos completos
@app.get("/vista-pedidos/", response_model=List[schemas.VistaPedido])
def obtener_vista_pedidos(db: Session = Depends(get_db)):
    try:
        return crud.obtener_vista_pedidos(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener vista de pedidos: {str(e)}")

@app.get("/")
def root():
    return {"mensaje": "API Tienda de Ropa funcionando correctamente"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)