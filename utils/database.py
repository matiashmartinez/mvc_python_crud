"""
Módulo para manejar la conexión a la base de datos SQLite.
"""
import sqlite3
import os
from typing import Optional
from utils.logger import setup_logger
import config

logger = setup_logger(__name__)


class DatabaseConnection:
    """
    Clase singleton para manejar la conexión a la base de datos.
    Implementa el patrón Singleton para tener una única instancia de conexión.
    """
    _instance: Optional['DatabaseConnection'] = None
    _connection: Optional[sqlite3.Connection] = None
    
    def __new__(cls) -> 'DatabaseConnection':
        """Implementación del patrón Singleton."""
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._initialize_database()
        return cls._instance
    
    def _initialize_database(self) -> None:
        """Inicializa la base de datos y crea las tablas si no existen."""
        try:
            os.makedirs(config.DB_DIR, exist_ok=True)
            
            self._connection = sqlite3.connect(config.DB_PATH)
            self._connection.row_factory = sqlite3.Row
            
            logger.info(f"Conexión establecida a {config.DB_PATH}")
            self._create_tables()
        except sqlite3.Error as e:
            logger.error(f"Error al inicializar base de datos: {e}")
            raise
    
    def _create_tables(self) -> None:
        """Crea las tablas necesarias en la base de datos."""
        try:
            cursor = self._connection.cursor()
            
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
            logger.info("Tablas creadas o verificadas exitosamente")
        except sqlite3.Error as e:
            logger.error(f"Error al crear tablas: {e}")
            raise
    
    def get_connection(self) -> sqlite3.Connection:
        """
        Obtiene la conexión a la base de datos.
        
        Returns:
            sqlite3.Connection: Conexión activa a la base de datos
        """
        return self._connection
    
    def close_connection(self) -> None:
        """Cierra la conexión a la base de datos."""
        try:
            if self._connection:
                self._connection.close()
                logger.info("Conexión a base de datos cerrada")
        except sqlite3.Error as e:
            logger.error(f"Error al cerrar conexión: {e}")
    
    def execute_query(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """
        Ejecuta una consulta SQL.
        
        Args:
            query (str): Consulta SQL a ejecutar
            params (tuple): Parámetros para la consulta
            
        Returns:
            sqlite3.Cursor: Cursor con el resultado de la consulta
        """
        try:
            cursor = self._connection.cursor()
            cursor.execute(query, params)
            self._connection.commit()
            return cursor
        except sqlite3.Error as e:
            logger.error(f"Error ejecutando consulta: {e}")
            raise