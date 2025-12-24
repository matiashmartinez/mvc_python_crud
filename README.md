# Sistema de Gestión de Clientes y Servicios

Aplicación desktop moderna construida con Python y PyQt6 para gestionar clientes y servicios utilizando arquitectura MVC.

## ✨ Características

- **Gestión de Clientes**: CRUD completo con validación de DNI y teléfono
- **Gestión de Servicios**: Manejo de servicios con 4 estados diferentes
- **Búsqueda Avanzada**: Filtros por nombre, apellido, DNI y estado
- **Base de Datos SQLite**: Persistencia con relaciones entre tablas
- **Interfaz Moderna**: Tema oscuro profesional con iconos intuitivos
- **Logging Completo**: Sistema de logs para debugging y auditoría
- **Validación Robusta**: Validación de entrada en todos los formularios

## 🚀 Inicio Rápido

### Requisitos
- Python 3.8+
- pip (gestor de paquetes de Python)

### Instalación

1. **Clonar o descargar el proyecto**
```bash
cd mvc_python_crud
```

2. **Crear entorno virtual** (recomendado)
```bash
python -m venv venv

# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación**
```bash
python main.py
```

## 📁 Estructura del Proyecto

```
mvc_python_crud/
├── models/              # Modelos de datos (Cliente, Servicio)
├── controllers/         # Lógica de negocio
├── views/              # Interfaz gráfica (PyQt6)
├── utils/              # Utilidades
│   ├── database.py     # Conexión SQLite
│   ├── styles.py       # Sistema de estilos
│   ├── icons.py        # Iconos Unicode
│   ├── logger.py       # Sistema de logging
│   └── validators.py   # Validadores
├── data/               # Base de datos SQLite
├── logs/               # Archivo de logs diarios
├── config.py           # Configuración centralizada
├── main.py             # Punto de entrada
└── requirements.txt    # Dependencias Python
```

## 🎨 Interfaz de Usuario

### Tema Oscuro Moderno
- Colores profesionales basados en azul (#2563EB)
- Iconos Unicode intuitivos en todos los botones
- Tema oscuro que reduce fatiga visual
- Transiciones suaves y efectos hover

### Componentes Principales

**MainWindow**:
- Header con título y logo
- Navbar con navegación entre vistas

**ClienteView**:
- Tabla de clientes con búsqueda y filtros
- Botones para CRUD (Nuevo, Editar, Eliminar)
- Actualización en tiempo real

**ServicioView**:
- Tabla de servicios con filtro por estado
- Gestión completa de servicios
- Asociación automática con clientes

## 📋 Uso Básico

### Crear un Cliente
1. Click en "Nuevo Cliente"
2. Completar formulario (Nombre, Apellido, DNI, Teléfono)
3. Click en "Guardar"

### Crear un Servicio
1. Click en "Nuevo Servicio"
2. Seleccionar cliente asociado
3. Completar detalles (Descripción, Estado, Fechas, Costo)
4. Click en "Guardar"

### Buscar Clientes
1. Usar el combo "Filtrar por:" para elegir criterio
2. Escribir el valor a buscar
3. La tabla se actualiza automáticamente

### Filtrar Servicios
1. Usar el combo "Filtrar por estado:"
2. Seleccionar estado deseado
3. La tabla muestra solo servicios con ese estado

## 🔧 Configuración

Editar `config.py` para personalizar:
- `DB_PATH`: Ubicación de la base de datos
- `LOG_LEVEL`: Nivel de logging (DEBUG, INFO, WARNING)
- `APP_NAME`: Nombre de la ventana
- `APP_WIDTH`, `APP_HEIGHT`: Dimensiones

También puede usar variables de entorno (ver `.env.example`).

## 📝 Logging

Los logs se guardan en `logs/app_YYYYMMDD.log`:
- Todas las operaciones de base de datos
- Errores y excepciones
- Validaciones y eventos importantes

## 🛠️ Desarrollo

### Estructura MVC
- **Models** (`models/`): Define estructura de datos
- **Controllers** (`controllers/`): Lógica de negocio y BD
- **Views** (`views/`): Interfaz gráfica y eventos

### Agregar Nueva Entidad
1. Crear modelo en `models/`
2. Crear controlador en `controllers/`
3. Crear vista en `views/`
4. Actualizar `main_window.py`

## 📚 Documentación Adicional

- `IMPROVEMENTS.md`: Cambios y mejoras implementadas
- `UI_IMPROVEMENTS.md`: Detalles del sistema de estilos

## 🐛 Solución de Problemas

**La aplicación no inicia**:
- Verificar que PyQt6 está instalado: `pip install -r requirements.txt`
- Revisar logs en carpeta `logs/`

**Base de datos corrupta**:
- Eliminar `data/database.db`
- Se recreará automáticamente al iniciar

**Error de permisos**:
- Asegurar que el directorio tiene permisos de lectura/escritura

## 📄 Licencia

Ver archivo `LICENSE` para más detalles.