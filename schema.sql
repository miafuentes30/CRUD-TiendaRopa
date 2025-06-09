
CREATE TYPE estado_pedido AS ENUM ('PENDIENTE', 'ENVIADO', 'ENTREGADO');
CREATE TYPE talla_ropa AS ENUM ('XS', 'S', 'M', 'L', 'XL', 'XXL');

-- Tabla de Clientes
CREATE TABLE clientes (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(15),
    fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE
);

-- Tabla de Productos
CREATE TABLE productos (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL CHECK (precio >= 0),
    talla talla_ropa
);

-- Tabla de Pedidos
CREATE TABLE pedidos (
    id_pedido SERIAL PRIMARY KEY,
    id_cliente INT REFERENCES clientes(id_cliente) ON DELETE CASCADE,
    fecha_pedido DATE NOT NULL DEFAULT CURRENT_DATE,
    estado estado_pedido NOT NULL DEFAULT 'PENDIENTE'
);

-- Tabla de Detalle de Pedidos
CREATE TABLE detalle_pedidos (
    id_detalle SERIAL PRIMARY KEY,
    id_pedido INT REFERENCES pedidos(id_pedido) ON DELETE CASCADE,
    id_producto INT REFERENCES productos(id_producto) ON DELETE CASCADE,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(10, 2) NOT NULL CHECK (precio_unitario >= 0)
);

-- Restricción UNIQUE para evitar duplicados en los pedidos
ALTER TABLE detalle_pedidos ADD CONSTRAINT unique_pedido_producto UNIQUE (id_pedido, id_producto);

-- Vista para mostrar información completa de pedidos
CREATE OR REPLACE VIEW vista_pedidos_completos AS
SELECT 
    p.id_pedido,
    c.nombre AS nombre_cliente,
    p.fecha_pedido,
    p.estado,
    pr.nombre AS nombre_producto,
    dp.cantidad,
    dp.precio_unitario,
    (dp.cantidad * dp.precio_unitario) AS subtotal
FROM 
    pedidos p
JOIN 
    clientes c ON p.id_cliente = c.id_cliente
JOIN 
    detalle_pedidos dp ON p.id_pedido = dp.id_pedido
JOIN 
    productos pr ON dp.id_producto = pr.id_producto;