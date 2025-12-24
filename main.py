"""
Punto de entrada principal de la aplicación.
"""
import sys
from PyQt6.QtWidgets import QApplication
from views.main_window import MainWindow
from utils.logger import setup_logger
import config

logger = setup_logger(__name__)


def main() -> None:
    """
    Función principal que inicia la aplicación.
    """
    try:
        logger.info("Iniciando aplicación...")
        
        app = QApplication(sys.argv)
        
        main_window = MainWindow()
        main_window.show()
        
        logger.info("Aplicación iniciada correctamente")
        sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"Error crítico en la aplicación: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()