"""
Vista para la gestión de clientes.
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLabel, QLineEdit,
                             QMessageBox, QDialog, QFormLayout, QComboBox,
                             QCheckBox, QHeaderView, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from controllers.cliente_controller import ClienteController
from utils.styles import get_stylesheet
from utils.icons import icon_button_text
from utils.export import ReportGenerator

class ClienteDialog(QDialog):
    """
    Diálogo para crear o editar un cliente.
    """
    
    def __init__(self, cliente=None, parent=None):
        """
        Inicializa el diálogo.
        
        Args:
            cliente: Instancia de Cliente a editar (None para crear nuevo)
            parent: Widget padre
        """
        super().__init__(parent)
        self.cliente = cliente
        self.controller = ClienteController()
        self.setStyleSheet(get_stylesheet())
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario."""
        title = "Editar Cliente" if self.cliente else "Nuevo Cliente"
        self.setWindowTitle(title)
        self.setMinimumWidth(450)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title_label = QLabel(icon_button_text("user", title))
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Ingrese el nombre...")
        self.apellido_input = QLineEdit()
        self.apellido_input.setPlaceholderText("Ingrese el apellido...")
        self.dni_input = QLineEdit()
        self.dni_input.setPlaceholderText("Ej: 12345678")
        self.telefono_input = QLineEdit()
        self.telefono_input.setPlaceholderText("Ej: 1123456789")
        self.baja_checkbox = QCheckBox("Marcar como inactivo")
        
        form_layout.addRow("👤 Nombre:", self.nombre_input)
        form_layout.addRow("👥 Apellido:", self.apellido_input)
        form_layout.addRow("🆔 DNI:", self.dni_input)
        form_layout.addRow("📞 Teléfono:", self.telefono_input)
        form_layout.addRow("", self.baja_checkbox)
        
        layout.addLayout(form_layout)
        layout.addSpacing(10)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.guardar_btn = QPushButton(icon_button_text("save", "Guardar"))
        self.guardar_btn.setMinimumHeight(40)
        self.guardar_btn.clicked.connect(self.guardar)
        
        self.cancelar_btn = QPushButton(icon_button_text("cancel", "Cancelar"))
        self.cancelar_btn.setMinimumHeight(40)
        self.cancelar_btn.setObjectName("dangerBtn")
        self.cancelar_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(self.guardar_btn)
        button_layout.addWidget(self.cancelar_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_data(self):
        """Carga los datos del cliente si está en modo edición."""
        if self.cliente:
            self.nombre_input.setText(self.cliente.nombre)
            self.apellido_input.setText(self.cliente.apellido)
            self.dni_input.setText(self.cliente.dni)
            self.telefono_input.setText(self.cliente.telefono)
            self.baja_checkbox.setChecked(self.cliente.baja)
    
    def guardar(self):
        """Guarda los datos del cliente."""
        # Obtener datos del formulario
        cliente_data = {
            'nombre': self.nombre_input.text().strip(),
            'apellido': self.apellido_input.text().strip(),
            'dni': self.dni_input.text().strip(),
            'telefono': self.telefono_input.text().strip(),
            'baja': self.baja_checkbox.isChecked()
        }
        
        # Validar datos
        if not cliente_data['nombre'] or not cliente_data['apellido'] or not cliente_data['dni']:
            QMessageBox.warning(self, "Error", "Nombre, apellido y DNI son obligatorios.")
            return
        
        # Guardar
        if self.cliente:
            # Modo edición
            success = self.controller.actualizar_cliente(self.cliente.id, cliente_data)
            if success:
                QMessageBox.information(self, "Éxito", "Cliente actualizado correctamente.")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "Error al actualizar el cliente.")
        else:
            # Modo creación
            nuevo_cliente = self.controller.crear_cliente(cliente_data)
            if nuevo_cliente:
                QMessageBox.information(self, "Éxito", "Cliente creado correctamente.")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "Error al crear el cliente.")

class ClienteView(QWidget):
    """
    Vista principal para la gestión de clientes.
    """
    
    def __init__(self):
        """Inicializa la vista de clientes."""
        super().__init__()
        self.controller = ClienteController()
        self.report_generator = ReportGenerator()
        self.setStyleSheet(get_stylesheet())
        self.init_ui()
        self.cargar_clientes()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title_label = QLabel("📋 Gestión de Clientes")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)
        
        search_label = QLabel(icon_button_text("filter", "Filtrar por:"))
        self.search_combo = QComboBox()
        self.search_combo.addItems(["Nombre", "Apellido", "DNI"])
        self.search_combo.setMaximumWidth(150)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ingrese el valor a buscar...")
        self.search_input.textChanged.connect(self.buscar_clientes)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_combo)
        search_layout.addWidget(self.search_input)
        search_layout.addStretch()
        
        layout.addLayout(search_layout)
        
        self.clientes_table = QTableWidget()
        self.clientes_table.setColumnCount(6)
        self.clientes_table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Apellido", "DNI", "Teléfono", "Estado"
        ])
        
        header = self.clientes_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.clientes_table.setColumnWidth(0, 0)
        self.clientes_table.horizontalHeader().hideSection(0)
        self.clientes_table.setAlternatingRowColors(True)
        self.clientes_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        layout.addWidget(self.clientes_table)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.nuevo_btn = QPushButton(icon_button_text("add", "Nuevo Cliente"))
        self.nuevo_btn.setMinimumHeight(40)
        self.nuevo_btn.clicked.connect(self.nuevo_cliente)
        
        self.editar_btn = QPushButton(icon_button_text("edit", "Editar"))
        self.editar_btn.setMinimumHeight(40)
        self.editar_btn.clicked.connect(self.editar_cliente)
        
        self.eliminar_btn = QPushButton(icon_button_text("delete", "Eliminar"))
        self.eliminar_btn.setMinimumHeight(40)
        self.eliminar_btn.setObjectName("dangerBtn")
        self.eliminar_btn.clicked.connect(self.eliminar_cliente)
        
        self.actualizar_btn = QPushButton(icon_button_text("refresh", "Actualizar"))
        self.actualizar_btn.setMinimumHeight(40)
        self.actualizar_btn.clicked.connect(self.cargar_clientes)
        
        self.exportar_btn = QPushButton(icon_button_text("download", "Exportar CSV"))
        self.exportar_btn.setMinimumHeight(40)
        self.exportar_btn.clicked.connect(self.exportar_clientes)
        
        button_layout.addWidget(self.nuevo_btn)
        button_layout.addWidget(self.editar_btn)
        button_layout.addWidget(self.eliminar_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.exportar_btn)
        button_layout.addWidget(self.actualizar_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def cargar_clientes(self):
        """Carga todos los clientes en la tabla."""
        clientes = self.controller.obtener_todos_clientes()
        self.clientes_table.setRowCount(len(clientes))
        
        for i, cliente in enumerate(clientes):
            self.clientes_table.setItem(i, 0, QTableWidgetItem(str(cliente.id)))
            self.clientes_table.setItem(i, 1, QTableWidgetItem(cliente.nombre))
            self.clientes_table.setItem(i, 2, QTableWidgetItem(cliente.apellido))
            self.clientes_table.setItem(i, 3, QTableWidgetItem(cliente.dni))
            self.clientes_table.setItem(i, 4, QTableWidgetItem(cliente.telefono))
            
            estado = "Activo" if not cliente.baja else "Inactivo"
            estado_item = QTableWidgetItem(estado)
            if cliente.baja:
                estado_item.setForeground(Qt.GlobalColor.red)
            else:
                estado_item.setForeground(Qt.GlobalColor.darkGreen)
            self.clientes_table.setItem(i, 5, estado_item)
    
    def buscar_clientes(self):
        """Busca clientes según el criterio seleccionado."""
        criterio = self.search_combo.currentText().lower()
        valor = self.search_input.text()
        
        if not valor:
            self.cargar_clientes()
            return
        
        clientes = self.controller.buscar_clientes(criterio, valor)
        self.clientes_table.setRowCount(len(clientes))
        
        for i, cliente in enumerate(clientes):
            self.clientes_table.setItem(i, 0, QTableWidgetItem(str(cliente.id)))
            self.clientes_table.setItem(i, 1, QTableWidgetItem(cliente.nombre))
            self.clientes_table.setItem(i, 2, QTableWidgetItem(cliente.apellido))
            self.clientes_table.setItem(i, 3, QTableWidgetItem(cliente.dni))
            self.clientes_table.setItem(i, 4, QTableWidgetItem(cliente.telefono))
            
            estado = "Activo" if not cliente.baja else "Inactivo"
            estado_item = QTableWidgetItem(estado)
            if cliente.baja:
                estado_item.setForeground(Qt.GlobalColor.red)
            else:
                estado_item.setForeground(Qt.GlobalColor.darkGreen)
            self.clientes_table.setItem(i, 5, estado_item)
    
    def obtener_cliente_seleccionado(self):
        """Obtiene el cliente seleccionado en la tabla."""
        selected_rows = self.clientes_table.selectionModel().selectedRows()
        if not selected_rows:
            return None
        
        row = selected_rows[0].row()
        cliente_id = int(self.clientes_table.item(row, 0).text())
        return self.controller.obtener_cliente(cliente_id)
    
    def exportar_clientes(self):
        """Exporta todos los clientes a CSV."""
        clientes = self.controller.obtener_todos_clientes(incluir_bajas=True)
        clientes_data = [c.to_dict() for c in clientes]
        
        filepath = self.report_generator.export_clientes_csv(clientes_data)
        if filepath:
            QMessageBox.information(
                self, 
                "Éxito", 
                f"Archivo exportado a:\n{filepath}"
            )
        else:
            QMessageBox.warning(self, "Error", "No se pudo exportar los clientes.")
    
    def nuevo_cliente(self):
        """Abre el diálogo para crear un nuevo cliente."""
        dialog = ClienteDialog()
        if dialog.exec():
            self.cargar_clientes()
    
    def editar_cliente(self):
        """Abre el diálogo para editar el cliente seleccionado."""
        cliente = self.obtener_cliente_seleccionado()
        if not cliente:
            QMessageBox.warning(self, "Advertencia", "Seleccione un cliente para editar.")
            return
        
        dialog = ClienteDialog(cliente, self)
        if dialog.exec():
            self.cargar_clientes()
    
    def eliminar_cliente(self):
        """Elimina el cliente seleccionado."""
        cliente = self.obtener_cliente_seleccionado()
        if not cliente:
            QMessageBox.warning(self, "Advertencia", "Seleccione un cliente para eliminar.")
            return
        
        # Confirmar eliminación
        reply = QMessageBox.question(
            self, "Confirmar",
            f"¿Está seguro de eliminar al cliente {cliente.nombre_completo}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success = self.controller.eliminar_cliente(cliente.id)
            if success:
                QMessageBox.information(self, "Éxito", "Cliente eliminado correctamente.")
                self.cargar_clientes()
            else:
                QMessageBox.critical(self, "Error", "Error al eliminar el cliente.")