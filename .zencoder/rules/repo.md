---
description: Repository Information Overview
alwaysApply: true
---

# MVC Python CRUD - Sistema de Gestión

## Summary

Desktop application built with Python and PyQt6 for managing clients and services using an MVC architecture. Features a SQLite database with complete CRUD operations, input validation, and a user-friendly GUI with tabbed navigation between clients and services management.

## Structure

```
mvc_python_crud/
├── models/              # Data models (Cliente, Servicio)
├── controllers/         # Business logic (CRUD operations)
├── views/              # UI components (PyQt6 dialogs and views)
├── utils/              # Helper utilities (database, validation, logging, UI)
├── data/               # SQLite database
├── logs/               # Application logs
├── config.py           # Centralized configuration
├── main.py             # Application entry point
├── requirements.txt    # Python dependencies
└── IMPROVEMENTS.md     # Change log of improvements
```

## Language & Runtime

**Language**: Python  
**Version**: 3.8+ (recommended: 3.10+)  
**Build System**: Standard Python (no compilation needed)  
**Package Manager**: pip

## Dependencies

**Main Dependencies**:
- PyQt6 (6.7.1) - Desktop GUI framework
- sqlite3 - Built-in database (no external package needed)

**Development Dependencies**: None required (uses standard library)

**Installation**:
```bash
pip install -r requirements.txt
```

## Build & Installation

1. **Setup virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run application**:
```bash
python main.py
```

Database is automatically initialized on first run in `data/database.db`

## Application Structure

**Entry Point**: `main.py:main()` - Initializes QApplication and displays MainWindow

**Main Components**:
- **ClienteView** (`views/cliente_view.py`) - Client management interface with table, CRUD dialogs
- **ServicioView** (`views/servicio_view.py`) - Service management with state tracking
- **DatabaseConnection** (`utils/database.py`) - Singleton pattern for SQLite connection
- **ClienteController** (`controllers/cliente_controller.py`) - Client business logic
- **ServicioController** (`controllers/servicio_controller.py`) - Service business logic

**Models**:
- **Cliente** - Attributes: id, nombre, apellido, dni, telefono, baja
- **Servicio** - Attributes: id, descripcion, estado, fecha_ingreso, fecha_estimada, costo, idCliente, baja

## Configuration

**File**: `config.py`

Environment variables (with defaults):
- `DB_PATH`: Database location (default: `data/database.db`)
- `LOG_LEVEL`: Logging level (default: `INFO`)
- `APP_NAME`: Window title
- `APP_WIDTH`: Window width
- `APP_HEIGHT`: Window height

Create `.env` file from `.env.example` to override defaults.

## Logging

**Configuration**: `utils/logger.py`

- Logs written to `logs/app_YYYYMMDD.log` (daily rotation)
- Console output for WARNING and ERROR levels
- File output for all levels (INFO+)
- All database operations, validations, and errors are logged

## Key Features

- **Client Management**: Create, read, update, delete clients with DNI/phone validation
- **Service Management**: Manage services with 4 states (PENDIENTE, EN_PROCESO, COMPLETADO, CANCELADO)
- **Search**: Search clients by name, surname, or DNI
- **Data Validation**: DNI (7-8 digits) and phone (8-15 digits) validation
- **Soft Deletes**: Logical deletion with `baja` flag instead of physical removal
- **Foreign Keys**: Services linked to clients with referential integrity

## Recent Improvements

### Code Quality
- Replaced all `print()` statements with structured logging
- Added complete return type hints to methods
- Fixed critical bug: Cliente `apellido` assignment (was assigning `nombre`)
- Removed duplicate imports

### Infrastructure
- Centralized configuration in `config.py`
- Logging system with daily file rotation
- Reusable UI helpers module to eliminate code duplication
- requirements.txt for easy dependency management

### Error Handling
- Try-catch blocks around database operations
- Proper exception logging with context
- SQLite error handling and re-raising for caller control

## Database Schema

**Tables**:
- `cliente`: id, nombre, apellido, dni (unique), telefono, baja
- `servicio`: id, descripcion, estado, fecha_ingreso, fecha_estimada, costo, idCliente (FK), baja

Automatically created on first database connection.
