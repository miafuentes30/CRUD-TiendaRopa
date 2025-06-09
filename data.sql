-- Clientes
INSERT INTO clientes (nombre, email, telefono, fecha_registro) VALUES
('Juan Pérez', 'juan@example.com', '555-1234', '2025-01-15'),
('María López', 'maria@example.com', '555-5678', '2025-02-20'),
('Carlos Ramírez', 'carlos@example.com', '555-9876', '2025-03-10'),
('Ana Torres', 'ana@example.com', '555-3456', '2025-04-05'),
('Luis Gómez', 'luis@example.com', '555-6789', '2025-04-10'),
('Juan Pérez', 'juan1@example.com', '555-1234', '2025-01-15'),
('María López', 'maria1@example.com', '555-5678', '2025-02-20'),
('Carlos Ramírez', 'carlos1@example.com', '555-9876', '2025-03-10'),
('Ana Torres', 'ana11@example.com', '555-3456', '2025-04-05'),
('Luis Gómez', 'luis1@example.com', '555-6789', '2025-04-10'),
('Juan Pérez', 'juan2@example.com', '555-1234', '2025-01-15'),
('María López', 'maria2@example.com', '555-5678', '2025-02-20'),
('Carlos Ramírez', 'carlos2@example.com', '555-9876', '2025-03-10'),
('Ana Torres', 'ana2@example.com', '555-3456', '2025-04-05'),
('Luis Gómez', 'luis2@example.com', '555-6789', '2025-04-10');

-- Productos
INSERT INTO productos (nombre, descripcion, precio, talla) VALUES
('Camisa de algodón', 'Camisa de manga larga', 29.99, 'M'),
('Pantalones vaqueros', 'Jeans clásicos', 39.99, 'L'),
('Vestido elegante', 'Vestido para ocasiones especiales', 49.99, 'S'),
('Sudadera con capucha', 'Sudadera cómoda y cálida', 34.99, 'XL'),
('Chaqueta impermeable', 'Ideal para la lluvia', 59.99, 'L'),
('Falda de mezclilla', 'Falda casual para diario', 24.99, 'M'),
('Blusa estampada', 'Blusa colorida y moderna', 27.99, 'S'),
('Shorts deportivos', 'Ropa cómoda para ejercitarse', 19.99, 'M'),
('Camiseta básica', 'Camiseta de algodón blanca', 14.99, 'L'),
('Bufanda tejida', 'Accesorio de invierno', 12.99, 'M');

-- Pedidos 
INSERT INTO pedidos (id_cliente, fecha_pedido, estado) VALUES
(1, '2025-04-01', 'ENVIADO'),     
(1, '2025-04-10', 'ENTREGADO'),   
(2, '2025-04-02', 'ENTREGADO'),   
(2, '2025-04-12', 'PENDIENTE'),   
(3, '2025-04-03', 'PENDIENTE'),   
(3, '2025-04-15', 'ENVIADO'),     
(4, '2025-04-04', 'ENTREGADO'),   
(4, '2025-04-18', 'PENDIENTE'),   
(5, '2025-04-06', 'ENVIADO'),
(5, '2025-04-20', 'ENTREGADO')
(8, '2025-04-12', 'PENDIENTE'),   
(9, '2025-04-03', 'PENDIENTE'),   
(6, '2025-04-15', 'ENVIADO'),     
(7, '2025-04-04', 'ENTREGADO'),   
(10, '2025-04-18', 'PENDIENTE'),   
(9, '2025-04-06', 'ENVIADO'), ;   

-- Detalle de pedidos
INSERT INTO detalle_pedidos (id_pedido, id_producto, cantidad, precio_unitario) VALUES
(1, 1, 2, 29.99),
(1, 2, 1, 39.99),
(2, 3, 1, 49.99),
(2, 4, 1, 34.99),
(3, 5, 1, 59.99),
(3, 6, 2, 24.99),
(4, 7, 1, 27.99),
(4, 1, 2, 29.99),
(5, 8, 3, 19.99),
(5, 9, 2, 14.99),
(6, 10, 1, 12.99),
(6, 3, 2, 49.99),
(7, 2, 1, 39.99),
(7, 5, 1, 59.99),
(8, 6, 2, 24.99),
(8, 8, 1, 19.99),
(9, 1, 1, 29.99),
(9, 4, 1, 34.99),
(10, 9, 1, 14.99),
(10, 10, 1, 12.99),
(2, 1, 1, 29.99), 
(3, 2, 1, 39.99), 
(4, 3, 1, 49.99),
(5, 4, 1, 34.99),
(6, 5, 1, 59.99),
(7, 6, 1, 24.99),
(8, 7, 1, 27.99);