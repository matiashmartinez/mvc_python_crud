"""
Ventana principal de la aplicación.
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QStackedWidget,
                             QMessageBox)
from views.cliente_view import ClienteView
from views.servicio_view import ServicioView

class MainWindow(QMainWindow):
    """
    Ventana principal que contiene las diferentes vistas de la aplicación.
    """
    
    def __init__(self):
        """Inicializa la ventana principal."""
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario."""
        self.setWindowTitle("Sistema de Gestión - Clientes y Servicios")
        self.setGeometry(100, 100, 1200, 700)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Barra de navegación
        nav_layout = QHBoxLayout()
        
        self.clientes_btn = QPushButton("Clientes")
        self.clientes_btn.setCheckable(True)
        self.clientes_btn.setChecked(True)
        self.clientes_btn.clicked.connect(self.mostrar_clientes)
        
        self.servicios_btn = QPushButton("Servicios")
        self.servicios_btn.setCheckable(True)
        self.servicios_btn.clicked.connect(self.mostrar_servicios)
        
        nav_layout.addWidget(self.clientes_btn)
        nav_layout.addWidget(self.servicios_btn)
        nav_layout.addStretch()
        
        main_layout.addLayout(nav_layout)
        
        # Widget apilado para cambiar entre vistas
        self.stacked_widget = QStackedWidget()
        
        # Crear vistas
        self.cliente_view = ClienteView()
        self.servicio_view = ServicioView()
        
        # Agregar vistas al widget apilado
        self.stacked_widget.addWidget(self.cliente_view)
        self.stacked_widget.addWidget(self.servicio_view)
        
        main_layout.addWidget(self.stacked_widget)
        
        # Estado inicial
        self.mostrar_clientes()
    
    def mostrar_clientes(self):
        """Muestra la vista de clientes."""
        self.clientes_btn.setChecked(True)
        self.servicios_btn.setChecked(False)
        self.stacked_widget.setCurrentIndex(0)
    
    def mostrar_servicios(self):
        """Muestra la vista de servicios."""
        self.clientes_btn.setChecked(False)
        self.servicios_btn.setChecked(True)
        self.stacked_widget.setCurrentIndex(1)
    
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