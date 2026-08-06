# Script de Base de Datos - PAT (pat_db)

Copia y pega el siguiente bloque de código directamente en MySQL Workbench, phpMyAdmin o la consola de MySQL para inicializar la base de datos completa.

```sql
-- ========================================================
-- CREACIÓN Y CONFIGURACIÓN INICIAL DE LA BASE DE DATOS
-- ========================================================

DROP DATABASE IF EXISTS pat_db;
CREATE DATABASE pat_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE pat_db;

-- =========================
-- ROLES Y USUARIOS
-- =========================

CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(255)
);

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    rol_id INT NOT NULL DEFAULT 1,
    activo BOOLEAN DEFAULT TRUE,
    token_recuperacion VARCHAR(255),
    token_expiracion DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rol_id) REFERENCES roles(id)
);

-- =========================
-- UBICACIÓN Y CLASIFICACIÓN
-- =========================

CREATE TABLE tipos_turismo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    icono VARCHAR(100)
);

CREATE TABLE departamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    codigo VARCHAR(10) UNIQUE
);

CREATE TABLE ciudades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    departamento_id INT NOT NULL,
    latitud DECIMAL(10,8),
    longitud DECIMAL(11,8),
    FOREIGN KEY (departamento_id) REFERENCES departamentos(id)
);

-- =========================
-- DESTINOS Y SERVICIOS
-- =========================

CREATE TABLE destinos_turisticos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT NOT NULL,
    ciudad_id INT NOT NULL,
    tipo_turismo_id INT,
    latitud DECIMAL(10,8),
    longitud DECIMAL(11,8),
    direccion VARCHAR(255),
    precio_entrada DECIMAL(10,2) DEFAULT 0.00,
    calificacion_promedio DECIMAL(3,2) DEFAULT 0.00,
    total_resenas INT DEFAULT 0,
    activo BOOLEAN DEFAULT TRUE,
    imagen_principal VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ciudad_id) REFERENCES ciudades(id),
    FOREIGN KEY (tipo_turismo_id) REFERENCES tipos_turismo(id)
);

CREATE TABLE hospedajes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    tipo ENUM('hotel','hostal','cabaña','apartamento','camping','otro') DEFAULT 'hotel',
    destino_id INT NOT NULL,
    direccion VARCHAR(255),
    precio_noche DECIMAL(10,2) NOT NULL,
    pagina_oficial VARCHAR(500) NULL,
    estrellas TINYINT,
    telefono VARCHAR(20),
    imagen_principal VARCHAR(255),
    activo BOOLEAN DEFAULT TRUE,
    latitud DECIMAL(10,8) NULL,
    longitud DECIMAL(11,8) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (destino_id) REFERENCES destinos_turisticos(id)
);

CREATE TABLE restaurantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    tipo_cocina VARCHAR(100),
    destino_id INT NOT NULL,
    direccion VARCHAR(255),
    precio_promedio DECIMAL(10,2),
    pagina_oficial VARCHAR(500) NULL,
    horario VARCHAR(255),
    imagen_principal VARCHAR(255) NULL,
    telefono VARCHAR(20),
    activo BOOLEAN DEFAULT TRUE,
    latitud DECIMAL(10,8) NULL,
    longitud DECIMAL(11,8) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (destino_id) REFERENCES destinos_turisticos(id)
);

CREATE TABLE actividades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    destino_id INT NOT NULL,
    direccion VARCHAR(255) NULL,
    precio DECIMAL(10,2) DEFAULT 0.00,
    pagina_oficial VARCHAR(500) NULL,
    telefono VARCHAR(30) NULL,
    imagen_principal VARCHAR(255) NULL,
    duracion_horas DECIMAL(5,2),
    dificultad ENUM('facil','moderado','dificil') DEFAULT 'facil',
    activa BOOLEAN DEFAULT TRUE,
    latitud DECIMAL(10,8) NULL,
    longitud DECIMAL(11,8) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (destino_id) REFERENCES destinos_turisticos(id)
);

-- =========================
-- TRANSPORTE
-- =========================

CREATE TABLE medios_transporte (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NULL,
    nombre VARCHAR(100) NOT NULL,
    velocidad_kmh DECIMAL(10,2) NOT NULL DEFAULT 60.00,
    costo_por_km DECIMAL(10,2) NOT NULL,
    icono VARCHAR(255),
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_transporte_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE
);

-- =========================
-- PLANES DE VIAJE Y ACTIVIDADES
-- =========================

CREATE TABLE planes_viaje (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    nombre_viaje VARCHAR(150) NOT NULL,
    origen VARCHAR(255) NOT NULL,
    latitud_origen DECIMAL(10,8),
    longitud_origen DECIMAL(11,8),
    destino_id INT NOT NULL,
    medio_transporte_id INT NOT NULL,
    fecha_inicio DATE,
    fecha_fin DATE,
    presupuesto DECIMAL(12,2) NULL,
    estado ENUM('planificado', 'en_progreso', 'finalizado', 'cancelado') DEFAULT 'planificado',
    num_personas INT DEFAULT 1,
    distancia_km DECIMAL(10,2),
    tiempo_horas DECIMAL(6,2),
    costo_transporte DECIMAL(10,2),
    notas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (destino_id) REFERENCES destinos_turisticos(id),
    FOREIGN KEY (medio_transporte_id) REFERENCES medios_transporte(id)
);

CREATE TABLE plan_actividades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    plan_id INT NOT NULL,
    actividad_id INT NOT NULL,
    FOREIGN KEY (plan_id) REFERENCES planes_viaje(id),
    FOREIGN KEY (actividad_id) REFERENCES actividades(id)
);

-- =========================
-- RESEÑAS
-- =========================

CREATE TABLE resenas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    destino_id INT NOT NULL,
    calificacion TINYINT NOT NULL,
    comentario TEXT,
    activa BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (destino_id) REFERENCES destinos_turisticos(id),
    UNIQUE KEY una_resena_por_usuario (usuario_id, destino_id)
);

-- =========================
-- DATOS INICIALES (SEEDS)
-- =========================

INSERT INTO roles (nombre, descripcion) VALUES
('usuario', 'Usuario regular'),
('administrador', 'Administrador del sistema'),
('proveedor', 'Proveedor de servicios'),
('guia', 'Guía turístico');

INSERT INTO departamentos (nombre, codigo) VALUES 
('Cundinamarca', '25'),
('Bolivar', '13');

INSERT INTO ciudades (nombre, departamento_id, latitud, longitud) VALUES
('Bogotá', 1, 4.71100000, -74.07210000),
('chia', 1, 4.86130000, -74.06020000),
('Cartagena', 2, 10.39972000, -75.51444000);

INSERT INTO tipos_turismo (nombre, icono) VALUES
('Naturaleza', '🌿'),
('Urbano', '🏙️'),
('Cultural', '🏛️'),
('Gastronómico', '🍽️'),
('Aventura', '🧗');

INSERT INTO medios_transporte (nombre, velocidad_kmh, costo_por_km, icono) VALUES
('Carro propio', 80.00, 400.00, '🚗'),
('Moto', 70.00, 200.00, '🏍️'),
('Bus intermunicipal', 65.00, 180.00, '🚌'),
('Avión', 800.00, 1200.00, '✈️');
