CREATE DATABASE IF NOT EXISTS techportfolio_db;
USE techportfolio_db;

-- Crea la tabla de mensajes
CREATE TABLE IF NOT EXISTS mensajes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    mensaje TEXT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO mensajes (nombre, email, mensaje) 
VALUES ('Usuario de Prueba', 'test@ejemplo.com', 'Hola, Este es un mensaje de prueba inicial.');