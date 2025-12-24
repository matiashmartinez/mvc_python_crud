"""
Configuración centralizada de la aplicación.
"""
import os

DB_PATH = os.getenv('DB_PATH', 'data/database.db')
DB_DIR = os.path.dirname(DB_PATH)
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

APP_NAME = "Sistema de Gestión - Clientes y Servicios"
APP_WIDTH = 1200
APP_HEIGHT = 700
