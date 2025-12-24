"""
Punto de entrada principal de la aplicación.
"""
import sys
from PyQt6.QtWidgets import QApplication
from views.main_window import MainWindow

def main():
    """
    Función principal que inicia la aplicación.
    """
    # Crear aplicación Qt
    app = QApplication(sys.argv)
    
    # Crear y mostrar ventana principal
    main_window = MainWindow()
    main_window.show()
    
    # Ejecutar loop de eventos
    sys.exit(app.exec())

if __name__ == "__main__":
    main()