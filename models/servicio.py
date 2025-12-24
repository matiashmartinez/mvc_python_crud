"""
Modelo Servicio.
"""
from datetime import datetime, date
from typing import Dict, Any, Optional
from .base_model import BaseModel

class Servicio(BaseModel):
    """
    Modelo que representa un servicio.
    
    Attributes:
        id (int): Identificador único del servicio
        descripcion (str): Descripción del servicio
        estado (str): Estado del servicio (PENDIENTE, EN_PROCESO, COMPLETADO, CANCELADO)
        fecha_ingreso (date): Fecha de ingreso del servicio
        fecha_estimada (date): Fecha estimada de finalización
        costo (float): Costo del servicio
        idCliente (int): ID del cliente asociado
        baja (bool): Estado del servicio (activo/inactivo)
    """
    
    ESTADOS = ['PENDIENTE', 'EN_PROCESO', 'COMPLETADO', 'CANCELADO']
    
    def __init__(self, id: Optional[int] = None, descripcion: str = "", 
                 estado: str = "PENDIENTE", fecha_ingreso: Optional[date] = None,
                 fecha_estimada: Optional[date] = None, costo: float = 0.0,
                 idCliente: Optional[int] = None, baja: bool = False):
        """
        Inicializa una instancia de Servicio.
        
        Args:
            id: Identificador único
            descripcion: Descripción del servicio
            estado: Estado del servicio
            fecha_ingreso: Fecha de ingreso
            fecha_estimada: Fecha estimada de finalización
            costo: Costo del servicio
            idCliente: ID del cliente asociado
            baja: Estado del servicio
        """
        self.id = id
        self.descripcion = descripcion
        self.estado = estado
        self.fecha_ingreso = fecha_ingreso or date.today()
        self.fecha_estimada = fecha_estimada
        self.costo = costo
        self.idCliente = idCliente
        self.baja = baja
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el objeto Servicio a diccionario.
        
        Returns:
            Dict con todos los atributos del servicio
        """
        return {
            'id': self.id,
            'descripcion': self.descripcion,
            'estado': self.estado,
            'fecha_ingreso': self.fecha_ingreso.isoformat() if self.fecha_ingreso else None,
            'fecha_estimada': self.fecha_estimada.isoformat() if self.fecha_estimada else None,
            'costo': self.costo,
            'idCliente': self.idCliente,
            'baja': self.baja
        }
    
    def from_dict(self, data: Dict[str, Any]) -> 'Servicio':
        """
        Carga los datos desde un diccionario.
        
        Args:
            data: Diccionario con los datos del servicio
            
        Returns:
            Self: Instancia actualizada
        """
        self.id = data.get('id')
        self.descripcion = data.get('descripcion', '')
        self.estado = data.get('estado', 'PENDIENTE')
        
        # Convertir strings a fechas
        fecha_ingreso = data.get('fecha_ingreso')
        if fecha_ingreso:
            if isinstance(fecha_ingreso, str):
                self.fecha_ingreso = date.fromisoformat(fecha_ingreso)
            else:
                self.fecha_ingreso = fecha_ingreso
        
        fecha_estimada = data.get('fecha_estimada')
        if fecha_estimada:
            if isinstance(fecha_estimada, str):
                self.fecha_estimada = date.fromisoformat(fecha_estimada)
            else:
                self.fecha_estimada = fecha_estimada
        
        self.costo = float(data.get('costo', 0.0))
        self.idCliente = data.get('idCliente')
        self.baja = data.get('baja', False)
        return self
    
    @classmethod
    def validate_data(cls, data: Dict[str, Any]) -> bool:
        """
        Valida los datos del servicio.
        
        Args:
            data: Diccionario con datos a validar
            
        Returns:
            bool: True si los datos son válidos
        """
        # Validar campos requeridos
        if not data.get('descripcion') or not data.get('idCliente'):
            return False
        
        # Validar estado
        if data.get('estado') not in cls.ESTADOS:
            return False
        
        # Validar costo
        try:
            costo = float(data.get('costo', 0))
            if costo < 0:
                return False
        except ValueError:
            return False
        
        # Validar fechas
        try:
            if data.get('fecha_ingreso'):
                if isinstance(data['fecha_ingreso'], str):
                    date.fromisoformat(data['fecha_ingreso'])
            
            if data.get('fecha_estimada'):
                if isinstance(data['fecha_estimada'], str):
                    date.fromisoformat(data['fecha_estimada'])
        except ValueError:
            return False
        
        return True
    
    def __str__(self) -> str:
        """Representación en string del servicio."""
        return f"Servicio #{self.id}: {self.descripcion} ({self.estado})"