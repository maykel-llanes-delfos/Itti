# Guía de Migración

## Del main.py monolítico al proyecto modular

### Cambios en los imports

#### Antes (main.py):

```python
from main import (
    AppConfig,
    GoogleAuthService,
    GoogleDriveService,
    GmailService,
    EmailProcessorJob,
    DriveMonitorJob,
    PlaceholderGenerator,
    Cliente,
)
```

#### Ahora (proyecto modular):

```python
from config import AppConfig
from services import GoogleAuthService, GoogleDriveService, GmailService
from jobs import EmailProcessorJob, DriveMonitorJob
from utils import PlaceholderGenerator
from models import Cliente
```

### Estructura de carpetas

```
Antes:
main.py (1500+ líneas)

Ahora:
├── config/settings.py
├── models/schemas.py
├── services/
│   ├── auth.py
│   ├── drive.py
│   └── gmail.py
├── jobs/
│   ├── email_processor.py
│   └── drive_monitor.py
├── utils/
│   ├── placeholder.py
│   └── callbacks.py
└── examples/
    ├── ejemplo_1_carpeta_placeholders.py
    ├── ejemplo_2_email_a_drive.py
    ├── ejemplo_3_monitorear_validar.py
    ├── ejemplo_4_leer_actualizar_excel.py
    └── ejemplo_5_flujo_completo.py
```

### Ventajas de la nueva estructura

1. **Modularidad**: Cada módulo tiene una responsabilidad clara
2. **Mantenibilidad**: Más fácil encontrar y modificar código
3. **Testabilidad**: Cada módulo se puede testear independientemente
4. **Escalabilidad**: Fácil agregar nuevos servicios o jobs
5. **Reutilización**: Los módulos se pueden importar donde se necesiten

### Pasos para migrar tu código

1. **Actualiza los imports** según la tabla de arriba

2. **Mueve tu código personalizado**:

   - Callbacks → `utils/callbacks.py`
   - Modelos → `models/schemas.py`
   - Configuración → `config/settings.py`

3. **Crea tus propios ejemplos** en `examples/`

4. **Mantén el main.py antiguo** como respaldo hasta verificar todo

### Ejemplo de migración

#### Código antiguo:

```python
# En main.py
from main import AppConfig, GoogleDriveService, GoogleAuthService

config = AppConfig()
auth = GoogleAuthService(config)
drive = GoogleDriveService(auth.get_credentials(), config)
```

#### Código nuevo:

```python
# En tu script
from config import AppConfig
from services import GoogleAuthService, GoogleDriveService

config = AppConfig()
auth = GoogleAuthService(config)
drive = GoogleDriveService(auth.get_credentials(), config)
```

### Compatibilidad

Todo el código funciona igual, solo cambian los imports.
No hay cambios en la API de las clases.
