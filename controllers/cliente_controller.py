"""
Controlador para manejar las operaciones CRUD de clientes.
"""
from typing import List, Optional, Dict, Any
from models.cliente import Cliente
from utils.database import DatabaseConnection
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ClienteController:
    """
    Controlador que maneja la lógica de negocio para los clientes.
    Actúa como intermediario entre las vistas y los modelos.
    """
    
    def __init__(self) -> None:
        """Inicializa el controlador con la conexión a la base de datos."""
        self.db = DatabaseConnection()
    
    def crear_cliente(self, cliente_data: Dict[str, Any]) -> Optional[Cliente]:
        """
        Crea un nuevo cliente en la base de datos.
        
        Args:
            cliente_data: Diccionario con los datos del cliente
            
        Returns:
            Cliente: Instancia del cliente creado o None si hay error
        """
        if not Cliente.validate_data(cliente_data):
            logger.warning(f"Datos de cliente inválidos: {cliente_data}")
            return None
        
        cliente = Cliente().from_dict(cliente_data)
        
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO cliente (nombre, apellido, dni, telefono, baja)
                VALUES (?, ?, ?, ?, ?)
            ''', (cliente.nombre, cliente.apellido, cliente.dni, 
                  cliente.telefono, cliente.baja))
            
            cliente.id = cursor.lastrowid
            conn.commit()
            
            logger.info(f"Cliente creado: ID={cliente.id}, DNI={cliente.dni}")
            return cliente
            
        except Exception as e:
            logger.error(f"Error al crear cliente: {e}")
            return None
    
    def obtener_cliente(self, cliente_id: int) -> Optional[Cliente]:
        """
        Obtiene un cliente por su ID.
        
        Args:
            cliente_id: ID del cliente a obtener
            
        Returns:
            Cliente: Instancia del cliente o None si no se encuentra
        """
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM cliente WHERE id = ? AND baja = 0
            ''', (cliente_id,))
            
            row = cursor.fetchone()
            
            if row:
                cliente = Cliente()
                cliente.from_dict(dict(row))
                return cliente
            
            return None
            
        except Exception as e:
            logger.error(f"Error al obtener cliente: {e}")
            return None
    
    def obtener_todos_clientes(self, incluir_bajas: bool = False) -> List[Cliente]:
        """
        Obtiene todos los clientes de la base de datos.
        
        Args:
            incluir_bajas: Si se incluyen clientes dados de baja
            
        Returns:
            List[Cliente]: Lista de clientes
        """
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            if incluir_bajas:
                cursor.execute('SELECT * FROM cliente')
            else:
                cursor.execute('SELECT * FROM cliente WHERE baja = 0')
            
            clientes = []
            for row in cursor.fetchall():
                cliente = Cliente()
                cliente.from_dict(dict(row))
                clientes.append(cliente)
            
            return clientes
            
        except Exception as e:
            logger.error(f"Error al obtener clientes: {e}")
            return []
    
    def actualizar_cliente(self, cliente_id: int, 
                          cliente_data: Dict[str, Any]) -> bool:
        """
        Actualiza los datos de un cliente.
        
        Args:
            cliente_id: ID del cliente a actualizar
            cliente_data: Nuevos datos del cliente
            
        Returns:
            bool: True si se actualizó correctamente
        """
        if not Cliente.validate_data(cliente_data):
            logger.warning(f"Datos inválidos para actualizar cliente {cliente_id}")
            return False
        
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE cliente 
                SET nombre = ?, apellido = ?, dni = ?, telefono = ?, baja = ?
                WHERE id = ?
            ''', (cliente_data['nombre'], cliente_data['apellido'],
                  cliente_data['dni'], cliente_data['telefono'],
                  cliente_data.get('baja', False), cliente_id))
            
            conn.commit()
            if cursor.rowcount > 0:
                logger.info(f"Cliente actualizado: ID={cliente_id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error al actualizar cliente {cliente_id}: {e}")
            return False
    
    def eliminar_cliente(self, cliente_id: int, logico: bool = True) -> bool:
        """
        Elimina un cliente de la base de datos.
        
        Args:
            cliente_id: ID del cliente a eliminar
            logico: Si es True, realiza baja lógica. Si es False, elimina físicamente.
            
        Returns:
            bool: True si se eliminó correctamente
        """
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            if logico:
                cursor.execute('''
                    UPDATE cliente SET baja = 1 WHERE id = ?
                ''', (cliente_id,))
            else:
                cursor.execute('DELETE FROM cliente WHERE id = ?', (cliente_id,))
            
            conn.commit()
            if cursor.rowcount > 0:
                logger.info(f"Cliente eliminado: ID={cliente_id}, lógico={logico}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error al eliminar cliente {cliente_id}: {e}")
            return False
    
    def obtener_ultimo_cliente(self) -> Optional[Cliente]:
        """
        Obtiene el último cliente creado.
        
        Returns:
            Cliente: Último cliente o None si no existe
        """
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM cliente WHERE baja = 0
                ORDER BY id DESC LIMIT 1
            ''')
            
            row = cursor.fetchone()
            
            if row:
                cliente = Cliente()
                cliente.from_dict(dict(row))
                return cliente
            
            return None
            
        except Exception as e:
            logger.error(f"Error al obtener último cliente: {e}")
            return None
    
    def buscar_clientes(self, criterio: str, 
                       valor: str) -> List[Cliente]:
        """
        Busca clientes por diferentes criterios.
        
        Args:
            criterio: Campo por el cual buscar (nombre, apellido, dni)
            valor: Valor a buscar
            
        Returns:
            List[Cliente]: Lista de clientes encontrados
        """
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            columnas_validas = {
                'nombre': 'nombre',
                'apellido': 'apellido',
                'dni': 'dni'
            }
            
            if criterio not in columnas_validas:
                logger.warning(f"Criterio de búsqueda inválido: {criterio}")
                return []
            
            columna = columnas_validas[criterio]
            
            cursor.execute(f'''
                SELECT * FROM cliente 
                WHERE {columna} LIKE ? AND baja = 0
            ''', (f'%{valor}%',))
            
            clientes = []
            for row in cursor.fetchall():
                cliente = Cliente()
                cliente.from_dict(dict(row))
                clientes.append(cliente)
            
            logger.info(f"Búsqueda: criterio={criterio}, resultados={len(clientes)}")
            return clientes
            
        except Exception as e:
            logger.error(f"Error al buscar clientes: {e}")
            return []