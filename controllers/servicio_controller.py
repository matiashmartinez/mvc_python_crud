"""
Controlador para manejar las operaciones CRUD de servicios.
"""
from typing import List, Optional, Dict, Any
from datetime import date
from models.servicio import Servicio
from utils.database import DatabaseConnection
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ServicioController:
    """
    Controlador que maneja la lógica de negocio para los servicios.
    """
    
    def __init__(self) -> None:
        """Inicializa el controlador con la conexión a la base de datos."""
        self.db = DatabaseConnection()
    
    def crear_servicio(self, servicio_data: Dict[str, Any]) -> Optional[Servicio]:
        """
        Crea un nuevo servicio en la base de datos.
        
        Args:
            servicio_data: Diccionario con los datos del servicio
            
        Returns:
            Servicio: Instancia del servicio creado o None si hay error
        """
        if not servicio_data.get('idCliente'):
            logger.warning("Servicio sin cliente asociado - operación rechazada")
            return None
        
        if not Servicio.validate_data(servicio_data):
            return None
        
        # Crear instancia del servicio
        servicio = Servicio().from_dict(servicio_data)
        
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Insertar en la base de datos
            cursor.execute('''
                INSERT INTO servicio 
                (descripcion, estado, fecha_ingreso, fecha_estimada, costo, idCliente, baja)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (servicio.descripcion, servicio.estado, 
                  servicio.fecha_ingreso, servicio.fecha_estimada,
                  servicio.costo, servicio.idCliente, servicio.baja))
            
            # Obtener el ID generado
            servicio.id = cursor.lastrowid
            conn.commit()
            
            return servicio
            
        except Exception as e:
            logger.error(f"Error al crear servicio: {e}")
            return None
    
    def obtener_servicio(self, servicio_id: int) -> Optional[Servicio]:
        """
        Obtiene un servicio por su ID.
        
        Args:
            servicio_id: ID del servicio a obtener
            
        Returns:
            Servicio: Instancia del servicio o None si no se encuentra
        """
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM servicio WHERE id = ? AND baja = 0
            ''', (servicio_id,))
            
            row = cursor.fetchone()
            
            if row:
                servicio = Servicio()
                servicio.from_dict(dict(row))
                return servicio
            
            return None
            
        except Exception as e:
            logger.error(f"Error al obtener servicio: {e}")
            return None
    
    def obtener_servicios_cliente(self, cliente_id: int, 
                                 incluir_bajas: bool = False) -> List[Servicio]:
        """
        Obtiene todos los servicios de un cliente específico.
        
        Args:
            cliente_id: ID del cliente
            incluir_bajas: Si se incluyen servicios dados de baja
            
        Returns:
            List[Servicio]: Lista de servicios del cliente
        """
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            if incluir_bajas:
                cursor.execute('''
                    SELECT * FROM servicio WHERE idCliente = ?
                ''', (cliente_id,))
            else:
                cursor.execute('''
                    SELECT * FROM servicio WHERE idCliente = ? AND baja = 0
                ''', (cliente_id,))
            
            servicios = []
            for row in cursor.fetchall():
                servicio = Servicio()
                servicio.from_dict(dict(row))
                servicios.append(servicio)
            
            return servicios
            
        except Exception as e:
            logger.error(f"Error al obtener servicios del cliente: {e}")
            return []
    
    def obtener_todos_servicios(self, incluir_bajas: bool = False) -> List[Servicio]:
        """
        Obtiene todos los servicios de la base de datos.
        
        Args:
            incluir_bajas: Si se incluyen servicios dados de baja
            
        Returns:
            List[Servicio]: Lista de servicios
        """
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            if incluir_bajas:
                cursor.execute('SELECT * FROM servicio')
            else:
                cursor.execute('SELECT * FROM servicio WHERE baja = 0')
            
            servicios = []
            for row in cursor.fetchall():
                servicio = Servicio()
                servicio.from_dict(dict(row))
                servicios.append(servicio)
            
            return servicios
            
        except Exception as e:
            logger.error(f"Error al obtener servicios: {e}")
            return []
    
    def actualizar_servicio(self, servicio_id: int, 
                           servicio_data: Dict[str, Any]) -> bool:
        """
        Actualiza los datos de un servicio.
        
        Args:
            servicio_id: ID del servicio a actualizar
            servicio_data: Nuevos datos del servicio
            
        Returns:
            bool: True si se actualizó correctamente
        """
        # Validar datos
        if not Servicio.validate_data(servicio_data):
            return False
        
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE servicio 
                SET descripcion = ?, estado = ?, fecha_ingreso = ?, 
                    fecha_estimada = ?, costo = ?, idCliente = ?, baja = ?
                WHERE id = ?
            ''', (servicio_data['descripcion'], servicio_data['estado'],
                  servicio_data['fecha_ingreso'], servicio_data.get('fecha_estimada'),
                  servicio_data['costo'], servicio_data['idCliente'],
                  servicio_data.get('baja', False), servicio_id))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            logger.error(f"Error al actualizar servicio: {e}")
            return False
    
    def eliminar_servicio(self, servicio_id: int, logico: bool = True) -> bool:
        """
        Elimina un servicio de la base de datos.
        
        Args:
            servicio_id: ID del servicio a eliminar
            logico: Si es True, realiza baja lógica. Si es False, elimina físicamente.
            
        Returns:
            bool: True si se eliminó correctamente
        """
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            if logico:
                # Baja lógica
                cursor.execute('''
                    UPDATE servicio SET baja = 1 WHERE id = ?
                ''', (servicio_id,))
            else:
                # Eliminación física
                cursor.execute('DELETE FROM servicio WHERE id = ?', (servicio_id,))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            logger.error(f"Error al eliminar servicio: {e}")
            return False
    
    def obtener_servicios_por_estado(self, estado: str) -> List[Servicio]:
        """
        Obtiene servicios filtrados por estado.
        
        Args:
            estado: Estado por el cual filtrar
            
        Returns:
            List[Servicio]: Lista de servicios encontrados
        """
        if estado not in Servicio.ESTADOS:
            return []
        
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM servicio 
                WHERE estado = ? AND baja = 0
                ORDER BY fecha_ingreso DESC
            ''', (estado,))
            
            servicios = []
            for row in cursor.fetchall():
                servicio = Servicio()
                servicio.from_dict(dict(row))
                servicios.append(servicio)
            
            return servicios
            
        except Exception as e:
            logger.error(f"Error al obtener servicios por estado: {e}")
            return []
    
    def actualizar_estado_servicio(self, servicio_id: int, 
                                  nuevo_estado: str) -> bool:
        """
        Actualiza solo el estado de un servicio.
        
        Args:
            servicio_id: ID del servicio
            nuevo_estado: Nuevo estado del servicio
            
        Returns:
            bool: True si se actualizó correctamente
        """
        if nuevo_estado not in Servicio.ESTADOS:
            return False
        
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE servicio 
                SET estado = ?
                WHERE id = ? AND baja = 0
            ''', (nuevo_estado, servicio_id))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            logger.error(f"Error al actualizar estado del servicio: {e}")
            return False