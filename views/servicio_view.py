"""
Vista para la gestión de servicios.
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLabel, QLineEdit,
                             QMessageBox, QDialog, QFormLayout, QComboBox,
                             QCheckBox, QDateEdit, QDoubleSpinBox, QSpinBox,
                             QHeaderView, QFrame)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from datetime import date

from controllers.cliente_controller import ClienteController
from controllers.servicio_controller import ServicioController
from models.servicio import Servicio
from utils.styles import get_stylesheet
from utils.icons import icon_button_text


class ServicioDialog(QDialog):
    """
    Diálogo para crear o editar un servicio.
    """
    
    def __init__(self, servicio=None, parent=None):
        """
        Inicializa el diálogo.
        
        Args:
            servicio: Instancia de Servicio a editar (None para crear nuevo)
            parent: Widget padre
        """
        super().__init__(parent)
        self.servicio = servicio
        self.servicio_controller = ServicioController()
        self.cliente_controller = ClienteController()
        self.setStyleSheet(get_stylesheet())
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario."""
        title = "Editar Servicio" if self.servicio else "Nuevo Servicio"
        self.setWindowTitle(title)
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title_label = QLabel(icon_button_text("service", title))
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        
        self.descripcion_input = QLineEdit()
        self.descripcion_input.setPlaceholderText("Descripción del servicio...")
        self.estado_combo = QComboBox()
        self.estado_combo.addItems(Servicio.ESTADOS)
        
        self.fecha_ingreso_input = QDateEdit()
        self.fecha_ingreso_input.setCalendarPopup(True)
        self.fecha_ingreso_input.setDate(QDate.currentDate())
        
        self.fecha_estimada_input = QDateEdit()
        self.fecha_estimada_input.setCalendarPopup(True)
        self.fecha_estimada_input.setDate(QDate.currentDate().addDays(7))
        
        self.costo_input = QDoubleSpinBox()
        self.costo_input.setRange(0, 999999.99)
        self.costo_input.setPrefix("$ ")
        self.costo_input.setDecimals(2)
        
        self.cliente_combo = QComboBox()
        self.cargar_clientes()
        
        self.baja_checkbox = QCheckBox("Marcar como inactivo")
        
        form_layout.addRow("📝 Descripción:", self.descripcion_input)
        form_layout.addRow("🔄 Estado:", self.estado_combo)
        form_layout.addRow("📅 Fecha Ingreso:", self.fecha_ingreso_input)
        form_layout.addRow("⏱️ Fecha Estimada:", self.fecha_estimada_input)
        form_layout.addRow("💵 Costo:", self.costo_input)
        form_layout.addRow("👤 Cliente:", self.cliente_combo)
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
    
    def cargar_clientes(self):
        """Carga los clientes activos en el combobox."""
        clientes = self.cliente_controller.obtener_todos_clientes()
        self.cliente_combo.clear()
        for cliente in clientes:
            self.cliente_combo.addItem(cliente.nombre_completo, cliente.id)
    
    def load_data(self):
        """Carga los datos del servicio si está en modo edición."""
        if self.servicio:
            self.descripcion_input.setText(self.servicio.descripcion)
            self.estado_combo.setCurrentText(self.servicio.estado)
            
            if self.servicio.fecha_ingreso:
                qdate = QDate(self.servicio.fecha_ingreso.year,
                             self.servicio.fecha_ingreso.month,
                             self.servicio.fecha_ingreso.day)
                self.fecha_ingreso_input.setDate(qdate)
            
            if self.servicio.fecha_estimada:
                qdate = QDate(self.servicio.fecha_estimada.year,
                             self.servicio.fecha_estimada.month,
                             self.servicio.fecha_estimada.day)
                self.fecha_estimada_input.setDate(qdate)
            
            self.costo_input.setValue(self.servicio.costo)
            
            # Seleccionar el cliente correspondiente
            index = self.cliente_combo.findData(self.servicio.idCliente)
            if index >= 0:
                self.cliente_combo.setCurrentIndex(index)
            
            self.baja_checkbox.setChecked(self.servicio.baja)
    
    def guardar(self):
        """Guarda los datos del servicio."""
        # Obtener datos del formulario
        servicio_data = {
            'descripcion': self.descripcion_input.text().strip(),
            'estado': self.estado_combo.currentText(),
            'fecha_ingreso': self.fecha_ingreso_input.date().toPyDate().isoformat(),
            'fecha_estimada': self.fecha_estimada_input.date().toPyDate().isoformat(),
            'costo': self.costo_input.value(),
            'idCliente': self.cliente_combo.currentData(),
            'baja': self.baja_checkbox.isChecked()
        }
        
        # Validar datos
        if not servicio_data['descripcion'] or not servicio_data['idCliente']:
            QMessageBox.warning(self, "Error", "Descripción y cliente son obligatorios.")
            return
        
        # Guardar
        if self.servicio:
            # Modo edición
            success = self.servicio_controller.actualizar_servicio(
                self.servicio.id, servicio_data
            )
            if success:
                QMessageBox.information(self, "Éxito", "Servicio actualizado correctamente.")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "Error al actualizar el servicio.")
        else:
            # Modo creación
            nuevo_servicio = self.servicio_controller.crear_servicio(servicio_data)
            if nuevo_servicio:
                QMessageBox.information(self, "Éxito", "Servicio creado correctamente.")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "Error al crear el servicio.")

class ServicioView(QWidget):
    """
    Vista principal para la gestión de servicios.
    """
    
    def __init__(self):
        """Inicializa la vista de servicios."""
        super().__init__()
        self.controller = ServicioController()
        self.setStyleSheet(get_stylesheet())
        self.init_ui()
        self.cargar_servicios()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title_label = QLabel("🔧 Gestión de Servicios")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(10)
        
        filter_label = QLabel(icon_button_text("filter", "Filtrar por estado:"))
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Todos", "PENDIENTE", "EN_PROCESO", "COMPLETADO", "CANCELADO"])
        self.filter_combo.setMaximumWidth(200)
        self.filter_combo.currentTextChanged.connect(self.filtrar_servicios)
        
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_combo)
        filter_layout.addStretch()
        
        layout.addLayout(filter_layout)
        
        self.servicios_table = QTableWidget()
        self.servicios_table.setColumnCount(8)
        self.servicios_table.setHorizontalHeaderLabels([
            "ID", "Descripción", "Estado", "F. Ingreso", "F. Estimada", 
            "Costo", "ID Cliente", "Estado"
        ])
        
        header = self.servicios_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents) # pyright: ignore[reportOptionalMemberAccess]
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed) # pyright: ignore[reportOptionalMemberAccess]
        self.servicios_table.setColumnWidth(0, 50)
        self.servicios_table.setAlternatingRowColors(True)
        self.servicios_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        layout.addWidget(self.servicios_table)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.nuevo_btn = QPushButton(icon_button_text("add", "Nuevo Servicio"))
        self.nuevo_btn.setMinimumHeight(40)
        self.nuevo_btn.clicked.connect(self.nuevo_servicio)
        
        self.editar_btn = QPushButton(icon_button_text("edit", "Editar"))
        self.editar_btn.setMinimumHeight(40)
        self.editar_btn.clicked.connect(self.editar_servicio)
        
        self.eliminar_btn = QPushButton(icon_button_text("delete", "Eliminar"))
        self.eliminar_btn.setMinimumHeight(40)
        self.eliminar_btn.setObjectName("dangerBtn")
        self.eliminar_btn.clicked.connect(self.eliminar_servicio)
        
        self.actualizar_btn = QPushButton(icon_button_text("refresh", "Actualizar"))
        self.actualizar_btn.setMinimumHeight(40)
        self.actualizar_btn.clicked.connect(self.cargar_servicios)
        
        button_layout.addWidget(self.nuevo_btn)
        button_layout.addWidget(self.editar_btn)
        button_layout.addWidget(self.eliminar_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.actualizar_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def cargar_servicios(self):
        """Carga todos los servicios en la tabla."""
        servicios = self.controller.obtener_todos_servicios()
        self.actualizar_tabla(servicios)
    
    def filtrar_servicios(self, estado):
        """Filtra servicios por estado."""
        if estado == "Todos":
            servicios = self.controller.obtener_todos_servicios()
        else:
            servicios = self.controller.obtener_servicios_por_estado(estado)
        
        self.actualizar_tabla(servicios)
    
    def actualizar_tabla(self, servicios):
        """Actualiza la tabla con la lista de servicios."""
        self.servicios_table.setRowCount(len(servicios))
        
        for i, servicio in enumerate(servicios):
            self.servicios_table.setItem(i, 0, QTableWidgetItem(str(servicio.id)))
            self.servicios_table.setItem(i, 1, QTableWidgetItem(servicio.descripcion))
            self.servicios_table.setItem(i, 2, QTableWidgetItem(servicio.estado))
            
            # Aplicar color según el estado
            estado_item = self.servicios_table.item(i, 2)
            if servicio.estado == "COMPLETADO":
                estado_item.setForeground(Qt.GlobalColor.darkGreen) # pyright: ignore[reportOptionalMemberAccess]
            elif servicio.estado == "CANCELADO":
                estado_item.setForeground(Qt.GlobalColor.red) # pyright: ignore[reportOptionalMemberAccess]
            elif servicio.estado == "EN_PROCESO":
                estado_item.setForeground(Qt.GlobalColor.blue) # pyright: ignore[reportOptionalMemberAccess]
            
            self.servicios_table.setItem(i, 3, 
                QTableWidgetItem(servicio.fecha_ingreso.isoformat() if servicio.fecha_ingreso else ""))
            
            self.servicios_table.setItem(i, 4, 
                QTableWidgetItem(servicio.fecha_estimada.isoformat() if servicio.fecha_estimada else ""))
            
            self.servicios_table.setItem(i, 5, 
                QTableWidgetItem(f"$ {servicio.costo:.2f}"))
            
            self.servicios_table.setItem(i, 6, QTableWidgetItem(str(servicio.idCliente)))
            
            estado_servicio = "Activo" if not servicio.baja else "Inactivo"
            estado_item = QTableWidgetItem(estado_servicio)
            if servicio.baja:
                estado_item.setForeground(Qt.GlobalColor.red)
            else:
                estado_item.setForeground(Qt.GlobalColor.darkGreen)
            self.servicios_table.setItem(i, 7, estado_item)
    
    def obtener_servicio_seleccionado(self):
        """Obtiene el servicio seleccionado en la tabla."""
        selected_rows = self.servicios_table.selectionModel().selectedRows() # type: ignore
        if not selected_rows:
            return None
        
        row = selected_rows[0].row()
        servicio_id = int(self.servicios_table.item(row, 0).text()) # type: ignore
        return self.controller.obtener_servicio(servicio_id)
    
    def nuevo_servicio(self):
        """Abre el diálogo para crear un nuevo servicio."""
        dialog = ServicioDialog()
        if dialog.exec():
            self.cargar_servicios()
    
    def editar_servicio(self):
        """Abre el diálogo para editar el servicio seleccionado."""
        servicio = self.obtener_servicio_seleccionado()
        if not servicio:
            QMessageBox.warning(self, "Advertencia", "Seleccione un servicio para editar.")
            return
        
        dialog = ServicioDialog(servicio, self)
        if dialog.exec():
            self.cargar_servicios()
    
    def eliminar_servicio(self):
        """Elimina el servicio seleccionado."""
        servicio = self.obtener_servicio_seleccionado()
        if not servicio:
            QMessageBox.warning(self, "Advertencia", "Seleccione un servicio para eliminar.")
            return
        
        # Confirmar eliminación
        reply = QMessageBox.question(
            self, "Confirmar",
            f"¿Está seguro de eliminar el servicio #{servicio.id}: {servicio.descripcion}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success = self.controller.eliminar_servicio(servicio.id) # type: ignore
            if success:
                QMessageBox.information(self, "Éxito", "Servicio eliminado correctamente.")
                self.cargar_servicios()
            else:
                QMessageBox.critical(self, "Error", "Error al eliminar el servicio.")