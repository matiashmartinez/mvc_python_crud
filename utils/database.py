"""
Módulo para manejar la conexión a la base de datos SQLite.
"""
import sqlite3
import os
from typing import Optional

class DatabaseConnection:
    """
    Clase singleton para manejar la conexión a la base de datos.
    Implementa el patrón Singleton para tener una única instancia de conexión.
    """
    _instance: Optional['DatabaseConnection'] = None
    _connection: Optional[sqlite3.Connection] = None
    
    def __new__(cls):
        """Implementación del patrón Singleton."""
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._initialize_database()
        return cls._instance
    
    def _initialize_database(self):
        """Inicializa la base de datos y crea las tablas si no existen."""
        # Crear directorio de datos si no existe
        os.makedirs('data', exist_ok=True)
        
        # Conectar a la base de datos
        self._connection = sqlite3.connect('data/database.db')
        self._connection.row_factory = sqlite3.Row  # Para acceder a las columnas por nombre
        
        # Crear tablas
        self._create_tables()
    
    def _create_tables(self):
        """Crea las tablas necesarias en la base de datos."""
        cursor = self._connection.cursor()
        
        # Tabla Cliente
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cliente (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                dni TEXT UNIQUE NOT NULL,
                telefono TEXT,
                baja BOOLEAN DEFAULT 0
            )
        ''')
        
        # Tabla Servicio
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS servicio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descripcion TEXT NOT NULL,
                estado TEXT DEFAULT 'PENDIENTE',
                fecha_ingreso DATE NOT NULL,
                fecha_estimada DATE,
                costo REAL DEFAULT 0.0,
                idCliente INTEGER NOT NULL,
                baja BOOLEAN DEFAULT 0,
                FOREIGN KEY (idCliente) REFERENCES cliente (id)
            )
        ''')
        
        self._connection.commit()
    
    def get_connection(self) -> sqlite3.Connection:
        """
        Obtiene la conexión a la base de datos.
        
        Returns:
            sqlite3.Connection: Conexión activa a la base de datos
        """
        return self._connection
    
    def close_connection(self):
        """Cierra la conexión a la base de datos."""
        if self._connection:
            self._connection.close()
    
    def execute_query(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """
        Ejecuta una consulta SQL.
        
        Args:
            query (str): Consulta SQL a ejecutar
            params (tuple): Parámetros para la consulta
            
        Returns:
            sqlite3.Cursor: Cursor con el resultado de la consulta
        """
        cursor = self._connection.cursor()
        cursor.execute(query, params)
        self._connection.commit()
        return cursor