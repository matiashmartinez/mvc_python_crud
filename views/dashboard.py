"""
Vista principal del dashboard.
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QPushButton, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from controllers.cliente_controller import ClienteController
from controllers.servicio_controller import ServicioController
from utils.styles import CURRENT_THEME
from utils.icons import icon_button_text


class StatCard(QFrame):
    """
    Tarjeta de estadística personalizada.
    """
    
    def __init__(self, title: str, value: str, subtitle: str = "", icon: str = "•"):
        """
        Inicializa la tarjeta de estadística.
        
        Args:
            title: Título de la estadística
            value: Valor principal
            subtitle: Subtítulo opcional
            icon: Icono Unicode
        """
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {CURRENT_THEME['surface']};
                border: 2px solid {CURRENT_THEME['border']};
                border-radius: 12px;
                padding: 20px;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        icon_label = QLabel(icon)
        icon_font = QFont()
        icon_font.setPointSize(32)
        icon_label.setFont(icon_font)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title_label = QLabel(title)
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setWeight(QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(f"color: {CURRENT_THEME['text_secondary']};")
        
        value_label = QLabel(value)
        value_font = QFont()
        value_font.setPointSize(28)
        value_font.setWeight(QFont.Weight.Bold)
        value_label.setFont(value_font)
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setStyleSheet(f"color: {CURRENT_THEME['primary']};")
        
        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        
        if subtitle:
            subtitle_label = QLabel(subtitle)
            subtitle_font = QFont()
            subtitle_font.setPointSize(10)
            subtitle_label.setFont(subtitle_font)
            subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            subtitle_label.setStyleSheet(f"color: {CURRENT_THEME['text_tertiary']};")
            layout.addWidget(subtitle_label)
        
        self.setLayout(layout)


class Dashboard(QWidget):
    """
    Vista del dashboard principal con estadísticas.
    """
    
    def __init__(self):
        """Inicializa el dashboard."""
        super().__init__()
        self.cliente_controller = ClienteController()
        self.servicio_controller = ServicioController()
        self.init_ui()
        self.cargar_estadisticas()
    
    def init_ui(self) -> None:
        """Inicializa la interfaz de usuario."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        title_label = QLabel("📊 Dashboard Principal")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        subtitle_label = QLabel("Resumen de estadísticas y actividad")
        subtitle_font = QFont()
        subtitle_font.setPointSize(12)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet(f"color: {CURRENT_THEME['text_secondary']};")
        layout.addWidget(subtitle_label)
        
        layout.addSpacing(10)
        
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)
        
        self.total_clientes_card = StatCard("Total Clientes", "0", icon="👥")
        self.clientes_activos_card = StatCard("Clientes Activos", "0", icon="✅")
        
        self.total_servicios_card = StatCard("Total Servicios", "0", icon="🔧")
        self.servicios_pendientes_card = StatCard("Pendientes", "0", icon="⏳")
        
        self.servicios_proceso_card = StatCard("En Proceso", "0", icon="⚙️")
        self.servicios_completados_card = StatCard("Completados", "0", icon="✔️")
        
        self.servicios_cancelados_card = StatCard("Cancelados", "0", icon="❌")
        self.costo_total_card = StatCard("Costo Total", "$0.00", icon="💵")
        
        grid_layout.addWidget(self.total_clientes_card, 0, 0)
        grid_layout.addWidget(self.clientes_activos_card, 0, 1)
        grid_layout.addWidget(self.total_servicios_card, 0, 2)
        grid_layout.addWidget(self.servicios_pendientes_card, 0, 3)
        
        grid_layout.addWidget(self.servicios_proceso_card, 1, 0)
        grid_layout.addWidget(self.servicios_completados_card, 1, 1)
        grid_layout.addWidget(self.servicios_cancelados_card, 1, 2)
        grid_layout.addWidget(self.costo_total_card, 1, 3)
        
        layout.addLayout(grid_layout)
        layout.addStretch()
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        refresh_btn = QPushButton("🔄  Actualizar")
        refresh_btn.setMinimumHeight(40)
        refresh_btn.setMinimumWidth(150)
        refresh_btn.clicked.connect(self.cargar_estadisticas)
        button_layout.addWidget(refresh_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def cargar_estadisticas(self) -> None:
        """Carga todas las estadísticas."""
        try:
            clientes = self.cliente_controller.obtener_todos_clientes()
            clientes_activos = len([c for c in clientes if not c.baja])
            
            self.total_clientes_card.findChild(QLabel).setText(str(len(clientes)))
            self.clientes_activos_card.findChild(QLabel).setText(str(clientes_activos))
            
            servicios = self.servicio_controller.obtener_todos_servicios()
            
            pendientes = len([s for s in servicios if s.estado == 'PENDIENTE'])
            proceso = len([s for s in servicios if s.estado == 'EN_PROCESO'])
            completados = len([s for s in servicios if s.estado == 'COMPLETADO'])
            cancelados = len([s for s in servicios if s.estado == 'CANCELADO'])
            
            costo_total = sum(s.costo for s in servicios)
            
            self.total_servicios_card.findChild(QLabel).setText(str(len(servicios)))
            self.servicios_pendientes_card.findChild(QLabel).setText(str(pendientes))
            self.servicios_proceso_card.findChild(QLabel).setText(str(proceso))
            self.servicios_completados_card.findChild(QLabel).setText(str(completados))
            self.servicios_cancelados_card.findChild(QLabel).setText(str(cancelados))
            self.costo_total_card.findChild(QLabel).setText(f"${costo_total:,.2f}")
        
        except Exception as e:
            print(f"Error cargando estadísticas: {e}")
