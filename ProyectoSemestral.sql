CREATE DATABASE IF NOT EXISTS EmpresaDB;
USE EmpresaDB;

-- Tabla Clientes
CREATE TABLE Clientes (
    rutCliente VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(100),
    direccion VARCHAR(150),
    email VARCHAR(100),
    telefono VARCHAR(20)
);

-- Tabla Facturas
CREATE TABLE Facturas (
    facturaID INT PRIMARY KEY,
    fechaEmision DATE,
    fechaVencimiento DATE,
    nombreCliente VARCHAR(100),
    totalNeto DECIMAL(10,2),
    totalIVA DECIMAL(10,2),
    total DECIMAL(10,2),
    ingreso DECIMAL(10,2),
    clasificacion VARCHAR(50),
    año YEAR,
    estado ENUM('Cancelado','Adeuda'),
    rutCliente VARCHAR(20),
    FOREIGN KEY (rutCliente) REFERENCES Clientes(rutCliente)
);

-- Tabla Equipos
CREATE TABLE Equipos (
    codigo VARCHAR(20) PRIMARY KEY,
    año YEAR,
    modelo VARCHAR(50),
    marca VARCHAR(50),
    estado ENUM('En arriendo', 'En taller', 'En reparacion')
);

-- Tabla Seguimientos
CREATE TABLE Seguimientos (
    codigo VARCHAR(20),            -- FK a Equipos
    fecha DATE,
    estado VARCHAR(50),
    cliente VARCHAR(100),
    obra VARCHAR(100),
    fechaEntrega DATE,
    dias INT,
    desde DATE,
    hasta DATE,
    guiaID INT PRIMARY KEY,
    facturaID INT,
    nota TEXT,
    FOREIGN KEY (codigo) REFERENCES Equipos(codigo),
    FOREIGN KEY (facturaID) REFERENCES Facturas(facturaID)
);

-- Tabla Cotizaciones
CREATE TABLE Cotizaciones (
    cotizacionID INT PRIMARY KEY,
    codigo VARCHAR(20),          -- FK a Equipos
    monto DECIMAL(12,2),
    fechaEmision DATE,
    rutCliente VARCHAR(20),      -- FK a Clientes
    FOREIGN KEY (codigo) REFERENCES Equipos(codigo),
    FOREIGN KEY (rutCliente) REFERENCES Clientes(rutCliente)
);

-- Tabla OrdenesTrabajo
CREATE TABLE OrdenesTrabajo (
    otID INT PRIMARY KEY,
    codigo VARCHAR(20),          -- FK a Equipos
    fechaEmision DATE,
    fechaInicio DATE,
    fechaTermino DATE,
    encargado VARCHAR(100),
    observaciones TEXT,
    FOREIGN KEY (codigo) REFERENCES Equipos(codigo)
);