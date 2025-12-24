"""
Utilidades para componentes UI reutilizables.
"""
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from typing import List, Callable, Tuple


def populate_table(
    table: QTableWidget,
    items: List,
    column_getters: List[Callable],
    color_rules: List[Tuple[int, Callable[[object], str]]] = []
) -> None:
    """
    Populate a table with items using provided column getters.
    
    Args:
        table: QTableWidget to populate
        items: List of items to display
        column_getters: List of functions to extract column values
        color_rules: List of (column_index, color_function) tuples for conditional coloring
    """
    table.setRowCount(len(items))
    
    for row_idx, item in enumerate(items):
        for col_idx, getter in enumerate(column_getters):
            cell_value = getter(item)
            table_item = QTableWidgetItem(str(cell_value))
            
            for col_rule, color_func in color_rules:
                if col_rule == col_idx:
                    table_item.setForeground(QColor(color_func(item)))
            
            table.setItem(row_idx, col_idx, table_item)
