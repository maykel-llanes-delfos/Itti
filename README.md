# Sistema de Gestión Google Drive y Gmail

Sistema modular para gestionar Google Drive y Gmail usando Service Accounts.

## 📁 Estructura del Proyecto

```
.
├── config/                 # Configuración
│   ├── __init__.py
│   └── settings.py        # AppConfig, AuthMode, GoogleScopes
│
├── models/                 # Modelos Pydantic
│   ├── __init__.py
│   └── schemas.py         # Cliente, ArchivoCliente, EmailMessage, etc.
│
├── services/               # Servicios de Google API
│   ├── __init__.py
│   ├── auth.py            # GoogleAuthService
│   ├── drive.py           # GoogleDriveService
│   └── gmail.py           # GmailService
│
├── jobs/                   # Jobs automatizados
│   ├── __init__.py
│   ├── email_processor.py # EmailProcessorJob
│   └── drive_monitor.py   # DriveMonitorJob
│
├── utils/                  # Utilidades
│   ├── __init__.py
│   ├── placeholder.py     # PlaceholderGenerator
│   └── callbacks.py       # Callbacks de ejemplo
│
├── examples/               # Ejemplos de uso
│   ├── ejemplo_1_carpeta_placeholders.py
│   ├── ejemplo_2_email_a_drive.py
│   ├── ejemplo_3_monitorear_validar.py
│   ├── ejemplo_4_leer_actualizar_excel.py
│   └── ejemplo_5_flujo_completo.py
│
├── main_refactored.py     # Punto de entrada principal
├── .env                    # Variables de entorno
└── service-account.json   # Credenciales de Service Account
```

## 🚀 Instalación

```bash
pip install google-api-python-client google-auth pydantic openpyxl pandas
```

## ⚙️ Configuración

1. Crea un archivo `.env`:

```env
AUTH_MODE=personal
SERVICE_ACCOUNT_FILE=service-account.json
DRIVE_ROOT_FOLDER_ID=tu_folder_id
GMAIL_FILTER_SUBJECT=
GMAIL_FILTER_FROM=
GMAIL_CHECK_INTERVAL=60
DRIVE_CHECK_INTERVAL=300
```

2. Coloca tu `service-account.json` en la raíz del proyecto

## 📚 Ejemplos de Uso

### Ejemplo 1: Crear carpeta con placeholders

```bash
python examples/ejemplo_1_carpeta_placeholders.py
```

### Ejemplo 2: Procesar correos y subir a Drive

```bash
python examples/ejemplo_2_email_a_drive.py
```

### Ejemplo 3: Monitorear cambios en Excel

```bash
python examples/ejemplo_3_monitorear_validar.py
```

### Ejemplo 4: Leer y actualizar Excel

```bash
python examples/ejemplo_4_leer_actualizar_excel.py
```

### Ejemplo 5: Flujo completo

```bash
python examples/ejemplo_5_flujo_completo.py
```

## 🔧 Uso Programático

```python
from config import AppConfig
from services import GoogleAuthService, GoogleDriveService
from models import Cliente

# Configuración
config = AppConfig()

# Autenticación
auth_service = GoogleAuthService(config)
credentials = auth_service.get_credentials()

# Servicio de Drive
drive_service = GoogleDriveService(credentials, config)

# Crear carpeta
cliente = Cliente(nombre="JUAN", apellido1="PEREZ", apellido2="LOPEZ")
folder_id = drive_service.crear_carpeta(cliente.nombre_carpeta)
```

## 📦 Módulos Principales

### Config

- `AppConfig`: Configuración desde variables de entorno
- `AuthMode`: PERSONAL o WORKSPACE
- `GoogleScopes`: Scopes de Google API

### Services

- `GoogleAuthService`: Autenticación con Service Accounts
- `GoogleDriveService`: Operaciones con Drive
- `GmailService`: Operaciones con Gmail

### Jobs

- `EmailProcessorJob`: Procesa correos y sube adjuntos
- `DriveMonitorJob`: Monitorea cambios en Excel

### Utils

- `PlaceholderGenerator`: Genera archivos de prueba
- Callbacks: Funciones de ejemplo para procesamiento

## 📝 Notas

- Para modo WORKSPACE necesitas domain-wide delegation
- Los callbacks son personalizables según tus necesidades
- Los jobs pueden ejecutarse en loop continuo o una sola vez
