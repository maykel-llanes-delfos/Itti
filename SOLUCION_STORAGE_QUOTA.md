# 🚨 Solución: Service Accounts no tienen storage quota

## ❌ Problema

```
Service Accounts do not have storage quota.
Leverage shared drives or use OAuth delegation instead.
```

## ✅ Soluciones Disponibles

### 1. 🎯 SOLUCIÓN RECOMENDADA: Usar Shared Drives

#### Paso 1: Crear un Shared Drive

1. Ve a [Google Drive](https://drive.google.com)
2. Click en "Nuevo" → "Más" → "Unidad compartida"
3. Dale un nombre: "Itti Storage" o similar
4. Créala

#### Paso 2: Agregar la Service Account al Shared Drive

1. Abre el Shared Drive que creaste
2. Click en el ícono de configuración (⚙️) → "Administrar miembros"
3. Click en "Agregar miembros"
4. Agrega el email de tu service account (está en service-account.json)
5. Dale permisos de "Editor" o "Administrador de contenido"

#### Paso 3: Obtener el ID del Shared Drive

1. Abre el Shared Drive
2. Copia el ID de la URL: `https://drive.google.com/drive/folders/ID_AQUI`
3. Actualiza tu `.env`:

```env
# Cambiar esta línea:
DRIVE_ROOT_FOLDER_ID=tu_shared_drive_id_aqui
```

### 2. 🔄 SOLUCIÓN ALTERNATIVA: OAuth con tu cuenta personal

#### Crear archivo oauth_setup.py:

```python
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os

SCOPES = ['https://www.googleapis.com/auth/drive']

def setup_oauth():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

if __name__ == '__main__':
    setup_oauth()
    print("✅ OAuth configurado correctamente")
```

#### Pasos para OAuth:

1. Ve a [Google Cloud Console](https://console.cloud.google.com)
2. APIs & Services → Credentials
3. Create Credentials → OAuth 2.0 Client ID
4. Application type: Desktop application
5. Descarga el JSON como `credentials.json`
6. Ejecuta: `python oauth_setup.py`

### 3. 🏢 SOLUCIÓN EMPRESARIAL: Google Workspace

Si tienes Google Workspace:

1. Configura domain-wide delegation
2. Cambia en `.env`: `AUTH_MODE=workspace`
3. Agrega tu email: `DELEGATED_USER_EMAIL=tu@empresa.com`

## 🚀 Implementación Rápida - Shared Drive

### Paso 1: Crear el Shared Drive

```bash
# Ve a Google Drive y crea un Shared Drive llamado "Itti Storage"
```

### Paso 2: Obtener email de Service Account

```python
import json

with open('service-account.json', 'r') as f:
    data = json.load(f)
    print(f"Email de Service Account: {data['client_email']}")
```

### Paso 3: Agregar Service Account al Shared Drive

1. Abre el Shared Drive
2. Configuración → Administrar miembros
3. Agregar: `el_email_que_aparecio_arriba@proyecto.iam.gserviceaccount.com`
4. Permisos: "Editor"

### Paso 4: Actualizar configuración

```env
# En tu .env, actualiza:
DRIVE_ROOT_FOLDER_ID=ID_DEL_SHARED_DRIVE
```

## 🔍 Script de Verificación

```python
# verificar_shared_drive.py
from config import AppConfig
from services import GoogleAuthService, GoogleDriveService

def verificar_shared_drive():
    config = AppConfig()
    auth = GoogleAuthService(config)
    drive = GoogleDriveService(auth.get_credentials(), config)

    try:
        # Intentar crear una carpeta de prueba
        folder_id = drive.crear_carpeta("TEST_FOLDER")
        print(f"✅ Carpeta creada: {folder_id}")

        # Intentar subir un archivo pequeño
        from utils import PlaceholderGenerator
        archivo = PlaceholderGenerator.crear_imagen_placeholder("test.png")
        file_id = drive.subir_archivo(archivo, folder_id)
        print(f"✅ Archivo subido: {file_id}")

        print("🎉 ¡Shared Drive funcionando correctamente!")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Asegúrate de que la Service Account esté agregada al Shared Drive")

if __name__ == "__main__":
    verificar_shared_drive()
```

## 📝 Resumen

**Problema**: Service Accounts no pueden subir archivos a Drive personal
**Solución más fácil**: Usar Shared Drives
**Tiempo estimado**: 5 minutos

1. Crear Shared Drive
2. Agregar Service Account como Editor
3. Actualizar DRIVE_ROOT_FOLDER_ID en .env
4. ¡Listo!
