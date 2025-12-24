"""
Sistema de exportación y reportes.
"""
import csv
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ReportGenerator:
    """
    Clase para generar reportes en diferentes formatos.
    """
    
    def __init__(self):
        """Inicializa el generador de reportes."""
        self.export_dir = Path("exports")
        self.export_dir.mkdir(exist_ok=True)
    
    def export_clientes_csv(self, clientes: List[Dict[str, Any]]) -> str:
        """
        Exporta clientes a CSV.
        
        Args:
            clientes: Lista de diccionarios con datos de clientes
        
        Returns:
            str: Ruta del archivo creado
        """
        if not clientes:
            logger.warning("No hay clientes para exportar")
            return ""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"clientes_{timestamp}.csv"
        filepath = self.export_dir / filename
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['Nombre', 'Apellido', 'DNI', 'Teléfono', 'Estado'])
                writer.writeheader()
                
                for cliente in clientes:
                    writer.writerow({
                        'Nombre': cliente.get('nombre', ''),
                        'Apellido': cliente.get('apellido', ''),
                        'DNI': cliente.get('dni', ''),
                        'Teléfono': cliente.get('telefono', ''),
                        'Estado': 'Activo' if not cliente.get('baja', False) else 'Inactivo'
                    })
            
            logger.info(f"Clientes exportados a {filepath}")
            return str(filepath)
        
        except Exception as e:
            logger.error(f"Error exportando clientes: {e}")
            return ""
    
    def export_servicios_csv(self, servicios: List[Dict[str, Any]]) -> str:
        """
        Exporta servicios a CSV.
        
        Args:
            servicios: Lista de diccionarios con datos de servicios
        
        Returns:
            str: Ruta del archivo creado
        """
        if not servicios:
            logger.warning("No hay servicios para exportar")
            return ""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"servicios_{timestamp}.csv"
        filepath = self.export_dir / filename
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'Descripción', 'Estado', 'Fecha Ingreso', 'Fecha Estimada', 
                    'Costo', 'Cliente ID', 'Estado Registro'
                ])
                writer.writeheader()
                
                for servicio in servicios:
                    writer.writerow({
                        'Descripción': servicio.get('descripcion', ''),
                        'Estado': servicio.get('estado', ''),
                        'Fecha Ingreso': servicio.get('fecha_ingreso', ''),
                        'Fecha Estimada': servicio.get('fecha_estimada', ''),
                        'Costo': servicio.get('costo', 0),
                        'Cliente ID': servicio.get('idCliente', ''),
                        'Estado Registro': 'Activo' if not servicio.get('baja', False) else 'Inactivo'
                    })
            
            logger.info(f"Servicios exportados a {filepath}")
            return str(filepath)
        
        except Exception as e:
            logger.error(f"Error exportando servicios: {e}")
            return ""
    
    def generate_resumen_servicios(self, servicios_por_estado: Dict[str, int], 
                                   total_costo: float) -> str:
        """
        Genera un resumen de servicios.
        
        Args:
            servicios_por_estado: Diccionario con conteos por estado
            total_costo: Costo total de servicios
        
        Returns:
            str: Ruta del archivo creado
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"resumen_servicios_{timestamp}.csv"
        filepath = self.export_dir / filename
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['RESUMEN DE SERVICIOS'])
                writer.writerow(['Fecha de Generación', datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
                writer.writerow([])
                
                writer.writerow(['Estado', 'Cantidad'])
                for estado, cantidad in servicios_por_estado.items():
                    writer.writerow([estado, cantidad])
                
                writer.writerow([])
                writer.writerow(['Costo Total', f"${total_costo:,.2f}"])
            
            logger.info(f"Resumen generado a {filepath}")
            return str(filepath)
        
        except Exception as e:
            logger.error(f"Error generando resumen: {e}")
            return ""
    
    def get_exports_dir(self) -> str:
        """
        Obtiene la ruta del directorio de exportaciones.
        
        Returns:
            str: Ruta del directorio
        """
        return str(self.export_dir.absolute())
