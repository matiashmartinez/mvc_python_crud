"""
Ventana principal de la aplicación.
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QStackedWidget,
                             QMessageBox, QLabel, QFrame)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from views.dashboard import Dashboard
from views.cliente_view import ClienteView
from views.servicio_view import ServicioView
from utils.logger import setup_logger
from utils.styles import get_stylesheet
from utils.icons import icon_button_text
import config

logger = setup_logger(__name__)


class MainWindow(QMainWindow):
    """
    Ventana principal que contiene las diferentes vistas de la aplicación.
    """
    
    def __init__(self) -> None:
        """Inicializa la ventana principal."""
        super().__init__()
        self.init_ui()
    
    def init_ui(self) -> None:
        """Inicializa la interfaz de usuario."""
        self.setWindowTitle(config.APP_NAME)
        self.setGeometry(100, 100, config.APP_WIDTH, config.APP_HEIGHT)
        self.setStyleSheet(get_stylesheet())
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header con logo y título
        header_widget = QFrame()
        header_widget.setMaximumHeight(70)
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(20, 10, 20, 10)
        
        title_label = QLabel("📊 Sistema de Gestión")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        main_layout.addWidget(header_widget)
        
        # Navbar
        nav_widget = QFrame()
        nav_widget.setMaximumHeight(50)
        nav_layout = QHBoxLayout(nav_widget)
        nav_layout.setContentsMargins(20, 0, 20, 0)
        nav_layout.setSpacing(10)
        
        self.dashboard_btn = QPushButton(icon_button_text("home", "Dashboard"))
        self.dashboard_btn.setCheckable(True)
        self.dashboard_btn.setMinimumHeight(40)
        self.dashboard_btn.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.dashboard_btn.clicked.connect(self.mostrar_dashboard)
        
        self.clientes_btn = QPushButton(icon_button_text("users", "Clientes"))
        self.clientes_btn.setCheckable(True)
        self.clientes_btn.setMinimumHeight(40)
        self.clientes_btn.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.clientes_btn.clicked.connect(self.mostrar_clientes)
        
        self.servicios_btn = QPushButton(icon_button_text("services", "Servicios"))
        self.servicios_btn.setCheckable(True)
        self.servicios_btn.setMinimumHeight(40)
        self.servicios_btn.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.servicios_btn.clicked.connect(self.mostrar_servicios)
        
        nav_layout.addWidget(self.dashboard_btn)
        nav_layout.addWidget(self.clientes_btn)
        nav_layout.addWidget(self.servicios_btn)
        nav_layout.addStretch()
        
        main_layout.addWidget(nav_widget)
        
        # Widget apilado
        self.stacked_widget = QStackedWidget()
        
        # Crear vistas
        self.dashboard_view = Dashboard()
        self.cliente_view = ClienteView()
        self.servicio_view = ServicioView()
        
        self.stacked_widget.addWidget(self.dashboard_view)
        self.stacked_widget.addWidget(self.cliente_view)
        self.stacked_widget.addWidget(self.servicio_view)
        
        main_layout.addWidget(self.stacked_widget)
        
        # Estado inicial
        self.mostrar_dashboard()
    
    def mostrar_dashboard(self) -> None:
        """Muestra la vista del dashboard."""
        self.dashboard_btn.setChecked(True)
        self.clientes_btn.setChecked(False)
        self.servicios_btn.setChecked(False)
        self.dashboard_view.cargar_estadisticas()
        self.stacked_widget.setCurrentIndex(0)
    
    def mostrar_clientes(self) -> None:
        """Muestra la vista de clientes."""
        self.dashboard_btn.setChecked(False)
        self.clientes_btn.setChecked(True)
        self.servicios_btn.setChecked(False)
        self.stacked_widget.setCurrentIndex(1)
    
    def mostrar_servicios(self) -> None:
        """Muestra la vista de servicios."""
        self.dashboard_btn.setChecked(False)
        self.clientes_btn.setChecked(False)
        self.servicios_btn.setChecked(True)
        self.stacked_widget.setCurrentIndex(2)
    
    def closeEvent(self, event): # type: ignore
        """
        Evento que se ejecuta al cerrar la ventana.
        
        Args:
            event: Evento de cierre
        """
        reply = QMessageBox.question(
            self, "Salir",
            "¿Está seguro de salir de la aplicación?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()