# 📊 Funcionalidad: Excel → Carpetas de Clientes

## 🎯 Objetivo

Procesar archivos Excel que contienen nombres de clientes y crear automáticamente carpetas en Google Drive, evitando duplicados.

## ✨ Características

### 1. Detección de Duplicados

- ✅ Lee nombres de clientes desde Excel
- ✅ Identifica clientes únicos (elimina duplicados)
- ✅ Verifica si la carpeta ya existe antes de crearla
- ✅ Usa cache para optimizar búsquedas

### 2. Procesamiento Inteligente

- ✅ Soporta múltiples hojas en Excel
- ✅ Configurable: especifica qué columna contiene los nombres
- ✅ Maneja nombres repetidos en diferentes filas
- ✅ Normaliza nombres (trim, uppercase, etc.)

### 3. Optimización

- ✅ Cache de carpetas existentes
- ✅ Búsqueda por lotes
- ✅ Evita llamadas redundantes a la API

## 🔧 Nuevos Métodos en GoogleDriveService

### `obtener_o_crear_carpeta(nombre_carpeta, parent_id)`

Obtiene una carpeta existente o la crea si no existe.

```python
folder_id = drive_service.obtener_o_crear_carpeta("JUAN PEREZ")
# Si existe: retorna el ID existente
# Si no existe: la crea y retorna el nuevo ID
```

### `listar_todas_carpetas(parent_id, actualizar_cache)`

Lista todas las carpetas y actualiza el cache.

```python
carpetas = drive_service.listar_todas_carpetas()
# Retorna: {"JUAN PEREZ": "folder_id_1", "MARIA GARCIA": "folder_id_2"}
```

### `procesar_clientes_desde_excel(excel_data, columna_nombre, crear_carpetas, parent_id)`

Procesa clientes desde Excel y crea/obtiene sus carpetas.

```python
carpetas = drive_service.procesar_clientes_desde_excel(
    excel_data=excel_data,
    columna_nombre="Nombre",
    crear_carpetas=True
)
# Retorna: {"JUAN PEREZ": "folder_id_1", "MARIA GARCIA": "folder_id_2"}
```

## 📚 Ejemplos Disponibles

### Ejemplo 6: Procesar Excel con clientes

```bash
python examples/ejemplo_6_procesar_excel_clientes.py
```

**Qué hace:**

- Crea un Excel de ejemplo con 10 registros (algunos duplicados)
- Identifica 6 clientes únicos
- Crea carpetas solo para los clientes únicos
- Muestra estadísticas del proceso

### Ejemplo 7: Procesar Excel existente

```bash
python examples/ejemplo_7_excel_existente.py
```

**Qué hace:**

- Lee un Excel que ya existe en Drive
- Procesa los clientes del Excel
- Crea carpetas para cada cliente único
- Configurable: especifica FILE_ID y COLUMNA_NOMBRE

### Ejemplo 8: Job automatizado

```bash
python examples/ejemplo_8_job_automatico.py
```

**Qué hace:**

- Monitorea una carpeta de Drive
- Detecta Excel nuevos o modificados
- Procesa clientes automáticamente
- Ejecuta callback para clientes nuevos
- Puede ejecutarse en loop continuo

## 🚀 Uso Básico

### 1. Procesar Excel simple

```python
from config import AppConfig
from services import GoogleAuthService, GoogleDriveService

# Setup
config = AppConfig()
auth = GoogleAuthService(config)
drive = GoogleDriveService(auth.get_credentials(), config)

# Leer Excel
excel_data = drive.leer_excel_desde_drive("FILE_ID_AQUI")

# Procesar clientes
carpetas = drive.procesar_clientes_desde_excel(
    excel_data=excel_data,
    columna_nombre="Nombre",  # Nombre de la columna
    crear_carpetas=True       # Crear si no existen
)

# Resultado
for nombre, folder_id in carpetas.items():
    print(f"{nombre}: {folder_id}")
```

### 2. Verificar si carpeta existe

```python
# Buscar carpeta existente
folder_id = drive.buscar_carpeta_por_nombre("JUAN PEREZ")

if folder_id:
    print(f"Carpeta existe: {folder_id}")
else:
    print("Carpeta no existe")
```

### 3. Obtener o crear carpeta

```python
# Obtiene si existe, crea si no
folder_id = drive.obtener_o_crear_carpeta("JUAN PEREZ")
print(f"Carpeta lista: {folder_id}")
```

## 🤖 Job Automatizado

### ExcelToFoldersJob

Job que monitorea Excel y crea carpetas automáticamente.

```python
from jobs import ExcelToFoldersJob

# Crear job
job = ExcelToFoldersJob(drive_service, config)

# Ejecutar una vez
carpetas_nuevas = job.procesar_excel_nuevos(
    folder_id="FOLDER_ID",
    columna_nombre="Nombre"
)

# O ejecutar en loop
job.ejecutar_loop(
    folder_id="FOLDER_ID",
    columna_nombre="Nombre",
    callback_on_new=mi_callback
)
```

### Callback personalizado

```python
def mi_callback(carpetas_nuevas):
    """Se ejecuta cuando hay clientes nuevos"""
    for nombre, folder_id in carpetas_nuevas.items():
        print(f"Nuevo cliente: {nombre}")

        # Aquí puedes:
        # - Enviar email de notificación
        # - Registrar en base de datos
        # - Crear archivos iniciales
        # - etc.
```

## 📊 Ejemplo de Excel

Tu Excel debe tener una columna con nombres de clientes:

| ID  | Nombre           | Email            | Telefono  |
| --- | ---------------- | ---------------- | --------- |
| 1   | JUAN PEREZ LOPEZ | juan@email.com   | 123456789 |
| 2   | MARIA GARCIA     | maria@email.com  | 987654321 |
| 3   | JUAN PEREZ LOPEZ | juan@email.com   | 123456789 |
| 4   | CARLOS MARTINEZ  | carlos@email.com | 555666777 |

**Resultado:**

- 4 registros en Excel
- 3 clientes únicos detectados
- 3 carpetas creadas (JUAN PEREZ LOPEZ solo una vez)

## 🔍 Flujo de Procesamiento

```
1. Leer Excel desde Drive
   ↓
2. Extraer nombres de columna especificada
   ↓
3. Eliminar duplicados (set)
   ↓
4. Listar carpetas existentes (cache)
   ↓
5. Para cada cliente único:
   ├─ Buscar en cache
   ├─ Si existe: usar carpeta existente
   └─ Si no existe: crear nueva carpeta
   ↓
6. Retornar diccionario {nombre: folder_id}
```

## ⚡ Optimizaciones

### Cache de carpetas

```python
# Primera búsqueda: consulta API
folder_id = drive.buscar_carpeta_por_nombre("JUAN PEREZ")

# Segunda búsqueda: usa cache (más rápido)
folder_id = drive.buscar_carpeta_por_nombre("JUAN PEREZ")
```

### Listar todas las carpetas primero

```python
# Cargar todas las carpetas en cache
drive.listar_todas_carpetas()

# Ahora todas las búsquedas usan cache
for nombre in clientes:
    folder_id = drive.obtener_o_crear_carpeta(nombre)
```

## 📝 Configuración

### En .env

```env
# Carpeta raíz donde se crearán las carpetas de clientes
DRIVE_ROOT_FOLDER_ID=tu_folder_id

# Intervalo de monitoreo (para jobs)
DRIVE_CHECK_INTERVAL=300
```

### En tu código

```python
# Especificar columna de nombres
columna_nombre = "Nombre"  # o "Cliente", "Razón Social", etc.

# Especificar carpeta padre
parent_id = "FOLDER_ID"  # o None para usar DRIVE_ROOT_FOLDER_ID
```

## 🎯 Casos de Uso

### 1. Onboarding de clientes

- Recibes Excel con clientes nuevos
- Script crea carpetas automáticamente
- Cada cliente tiene su espacio en Drive

### 2. Migración de datos

- Tienes Excel con todos tus clientes
- Script crea estructura de carpetas
- Evita duplicados si ejecutas varias veces

### 3. Monitoreo continuo

- Job monitorea carpeta de Drive
- Detecta Excel nuevos/modificados
- Crea carpetas automáticamente
- Notifica cuando hay clientes nuevos

## 🔧 Personalización

### Normalización de nombres

Puedes agregar lógica personalizada:

```python
def normalizar_nombre(nombre):
    """Normaliza nombre de cliente"""
    nombre = nombre.strip().upper()
    nombre = nombre.replace("  ", " ")  # Espacios dobles
    # Agregar más lógica según necesites
    return nombre
```

### Estructura de carpetas

Puedes crear subcarpetas:

```python
# Crear carpeta principal
folder_id = drive.obtener_o_crear_carpeta("JUAN PEREZ")

# Crear subcarpetas
drive.crear_carpeta("Documentos", parent_id=folder_id)
drive.crear_carpeta("Facturas", parent_id=folder_id)
drive.crear_carpeta("Contratos", parent_id=folder_id)
```

## ✅ Ventajas

1. **Evita duplicados**: No crea carpetas que ya existen
2. **Optimizado**: Usa cache para reducir llamadas a API
3. **Flexible**: Configurable para diferentes estructuras de Excel
4. **Automatizable**: Puede ejecutarse como job continuo
5. **Escalable**: Maneja grandes cantidades de clientes

## 📚 Documentación Adicional

- Ver ejemplos en `examples/ejemplo_6_*.py`
- Ver código en `services/drive.py`
- Ver job en `jobs/excel_to_folders.py`
