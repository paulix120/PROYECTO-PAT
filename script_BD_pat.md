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

select * from usuarios;
DELETE FROM usuarios WHERE id = 4;

INSERT INTO roles (nombre, descripcion) VALUES
('usuario', 'Usuario regular'),
('administrador', 'Administrador del sistema'),
('proveedor', 'Proveedor de servicios'),
('guia', 'Guía turístico');

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
INSERT INTO departamentos (nombre, codigo)
VALUES ('Cundinamarca', '25');
INSERT INTO departamentos (nombre, codigo)
VALUES ('Bolivar', '13');

select * from departamentos; 

CREATE TABLE ciudades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    departamento_id INT NOT NULL,
    latitud DECIMAL(10,8),
    longitud DECIMAL(11,8),
    FOREIGN KEY (departamento_id) REFERENCES departamentos(id)
);
INSERT INTO ciudades (nombre, departamento_id, latitud, longitud)
VALUES
('Bogotá', 1, 4.71100000, -74.07210000);
INSERT INTO ciudades (nombre, departamento_id, latitud, longitud)
VALUES
('chia', 1, 4.86130000, -74.06020000);

INSERT INTO ciudades (nombre, departamento_id, latitud, longitud)
VALUES
('Cartagena', 2, 0, 0);

select * from ciudades;
-- =========================
-- DESTINOS
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

-- =========================
-- SERVICIOS TURÍSTICOS
-- =========================

CREATE TABLE hospedajes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    tipo ENUM('hotel','hostal','cabaña','apartamento','camping','otro') DEFAULT 'hotel',
    destino_id INT NOT NULL,
    direccion VARCHAR(255),
    
    precio_noche DECIMAL(10,2) NOT NULL,
-- se puede modificar: 
-- 1. precio por tipo de habitacion

    estrellas TINYINT,
    telefono VARCHAR(20),
    imagen_principal VARCHAR(255),
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (destino_id) REFERENCES destinos_turisticos(id)
);
ALTER TABLE hospedajes
ADD COLUMN latitud DECIMAL(10,8) NULL,
ADD COLUMN longitud DECIMAL(11,8) NULL;
ALTER TABLE hospedajes
ADD COLUMN pagina_oficial VARCHAR(500) NULL
AFTER precio_noche;


CREATE TABLE restaurantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    tipo_cocina VARCHAR(100),
    destino_id INT NOT NULL,
    direccion VARCHAR(255),
    
    precio_promedio DECIMAL(10,2),
-- precio por revisar
    
    horario VARCHAR(255),
    telefono VARCHAR(20),
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (destino_id) REFERENCES destinos_turisticos(id)
);
ALTER TABLE restaurantes
ADD COLUMN pagina_oficial VARCHAR(500) NULL AFTER precio_promedio,
ADD COLUMN imagen_principal VARCHAR(255) NULL AFTER horario,
ADD COLUMN latitud DECIMAL(10,8) NULL AFTER activo,
ADD COLUMN longitud DECIMAL(11,8) NULL AFTER latitud;

CREATE TABLE actividades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    destino_id INT NOT NULL,
    precio DECIMAL(10,2) DEFAULT 0.00,
    duracion_horas DECIMAL(5,2),
    dificultad ENUM('facil','moderado','dificil') DEFAULT 'facil',
    activa BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (destino_id) REFERENCES destinos_turisticos(id)
);
ALTER TABLE actividades
ADD COLUMN direccion VARCHAR(255) NULL AFTER destino_id,
ADD COLUMN pagina_oficial VARCHAR(500) NULL AFTER precio,
ADD COLUMN telefono VARCHAR(30) NULL AFTER pagina_oficial,
ADD COLUMN imagen_principal VARCHAR(255) NULL AFTER telefono,
ADD COLUMN latitud DECIMAL(10,8) NULL AFTER activa,
ADD COLUMN longitud DECIMAL(11,8) NULL AFTER latitud;

-- =========================
-- TRANSPORTE
-- =========================
DROP TABLE medios_transporte;
CREATE TABLE medios_transporte (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NULL,
    nombre VARCHAR(100) NOT NULL,
    velocidad_kmh DECIMAL(10,2) NOT NULL DEFAULT 60,
    costo_por_km DECIMAL(10,2) NOT NULL,
    icono VARCHAR(255),
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_transporte_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE
);
ALTER TABLE medios_transporte
ADD activo BOOLEAN NOT NULL DEFAULT TRUE;
ALTER TABLE medios_transporte
ADD COLUMN usuario_id INT NULL AFTER id;
ALTER TABLE medios_transporte
ADD CONSTRAINT fk_transporte_usuario
FOREIGN KEY (usuario_id)
REFERENCES usuarios(id)
ON DELETE CASCADE;
-- =========================
-- PLANES DE VIAJE (MEJORADO)
-- =========================

CREATE TABLE planes_viaje (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    nombre VARCHAR(150) NOT NULL,

    origen VARCHAR(255) NOT NULL,
    latitud_origen DECIMAL(10,8),
    longitud_origen DECIMAL(11,8),

    destino_id INT NOT NULL,
    hospedaje_id INT,  

    medio_transporte_id INT,
    fecha_salida DATE,
    fecha_regreso DATE,
    num_personas INT DEFAULT 1,

    distancia_km DECIMAL(10,2),
    tiempo_horas DECIMAL(6,2),

    costo_transporte DECIMAL(10,2),
    costo_hospedaje DECIMAL(10,2),
    costo_total_estimado DECIMAL(10,2),

    notas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (destino_id) REFERENCES destinos_turisticos(id),
    FOREIGN KEY (medio_transporte_id) REFERENCES medios_transporte(id),
    FOREIGN KEY (hospedaje_id) REFERENCES hospedajes(id)  -- ✅ RELACIÓN AGREGADA
);

ALTER TABLE planes_viaje
DROP FOREIGN KEY planes_viaje_ibfk_4;
ALTER TABLE planes_viaje
DROP INDEX hospedaje_id;
ALTER TABLE planes_viaje
DROP COLUMN hospedaje_id,
DROP COLUMN costo_hospedaje,
DROP COLUMN costo_total_estimado;
ALTER TABLE planes_viaje
CHANGE nombre nombre_viaje VARCHAR(150) NOT NULL,
CHANGE fecha_salida fecha_inicio DATE,
CHANGE fecha_regreso fecha_fin DATE;
ALTER TABLE planes_viaje
ADD COLUMN presupuesto DECIMAL(12,2) NULL
AFTER fecha_fin,
ADD COLUMN estado ENUM(
'planificado',
'en_progreso',
'finalizado',
'cancelado'
)
DEFAULT 'planificado'
AFTER presupuesto;
ALTER TABLE planes_viaje
MODIFY medio_transporte_id INT NOT NULL;

-- =========================
-- ACTIVIDADES DEL PLAN (NUEVA TABLA)
-- =========================

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
-- DATOS INICIALES
-- =========================

INSERT INTO tipos_turismo (nombre, icono) VALUES
('Naturaleza', '🌿'),
('Urbano', '🏙️'),
('Cultural', '🏛️'),
('Gastronómico', '🍽️'),
('Aventura', '🧗');

INSERT INTO medios_transporte (nombre, velocidad_kmh, costo_por_km, icono) VALUES
('Carro propio', 80, 400, '🚗'),
('Moto', 70, 200, '🏍️'),
('Bus intermunicipal', 65, 180, '🚌'),
('Avión', 800, 1200, '✈️');

select * from medios_transporte;