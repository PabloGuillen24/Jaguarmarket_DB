CREATE DATABASE IF NOT EXISTS jaguarmarket CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE jaguarmarket;

CREATE TABLE IF NOT EXISTS auth_user (
    id INT PRIMARY KEY,
    password VARCHAR(128),
    last_login DATETIME,
    is_superuser BOOLEAN,
    username VARCHAR(150),
    last_name VARCHAR(150),
    email VARCHAR(254),
    is_staff BOOLEAN,
    is_active BOOLEAN,
    date_joined DATETIME,
    first_name VARCHAR(150)
);

CREATE TABLE IF NOT EXISTS productos_categoria (
    id INT PRIMARY KEY,
    nombre VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS productos_producto (
    id INT PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT,
    precio DECIMAL(10, 2),
    categoria_id INT,
    publicado_por_id INT,
    imagen VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS productos_perfilusuario (
    id INT PRIMARY KEY,
    carrera VARCHAR(100),
    usuario_id INT,
    telefono VARCHAR(15),
    foto VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS productos_mensaje (
    id INT PRIMARY KEY,
    contenido TEXT,
    timestamp DATETIME,
    emisor_id INT,
    producto_id INT,
    receptor_id INT,
    leido BOOLEAN
);

ALTER TABLE productos_producto
  ADD FOREIGN KEY (categoria_id) REFERENCES productos_categoria(id),
  ADD FOREIGN KEY (publicado_por_id) REFERENCES auth_user(id);

ALTER TABLE productos_perfilusuario
  ADD FOREIGN KEY (usuario_id) REFERENCES auth_user(id);

ALTER TABLE productos_mensaje
  ADD FOREIGN KEY (emisor_id) REFERENCES auth_user(id),
  ADD FOREIGN KEY (producto_id) REFERENCES productos_producto(id),
  ADD FOREIGN KEY (receptor_id) REFERENCES auth_user(id);
