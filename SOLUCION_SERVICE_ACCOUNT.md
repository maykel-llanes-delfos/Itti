# Solución: Service Account sin cuota de almacenamiento

## ❌ Problema

```
Service Accounts do not have storage quota.
```

Las Service Accounts no tienen almacenamiento propio en Google Drive.

## ✅ Solución para Uso Personal

### Paso 1: Obtener el email de tu Service Account

1. Abre el archivo `light-height-drive-235716-82ec9163785a.json`
2. Busca el campo `"client_email"`, ejemplo:
   ```json
   "client_email": "tu-service-account@project-id.iam.gserviceaccount.com"
   ```
3. Copia ese email

### Paso 2: Compartir la carpeta de Drive

1. Abre Google Drive en tu navegador
2. Ve a la carpeta con ID: `1dx6X_bSNURDzVbUqVIi4GAOfkFWBCKXX`
   - URL: https://drive.google.com/drive/folders/1dx6X_bSNURDzVbUqVIi4GAOfkFWBCKXX
3. Click derecho → "Compartir" o botón "Compartir"
4. Pega el email de la Service Account
5. Dale permisos de **"Editor"**
6. Click en "Enviar"

### Paso 3: Probar de nuevo

```bash
python examples\ejemplo_1_carpeta_placeholders.py
```

¡Ahora debería funcionar!

## 🏢 Solución para Google Workspace

Si tienes Google Workspace, tienes dos opciones:

### Opción 1: Usar Shared Drives (Recomendado)

1. Crea un Shared Drive en tu Workspace
2. Comparte el Shared Drive con la Service Account
3. Usa el ID del Shared Drive en `DRIVE_ROOT_FOLDER_ID`

### Opción 2: Domain-Wide Delegation

1. Configura domain-wide delegation en Google Workspace Admin
2. Cambia en `.env`:
   ```env
   AUTH_MODE=workspace
   DELEGATED_USER_EMAIL=tu-email@tuempresa.com
   ```

## 📝 Verificar que funciona

Después de compartir la carpeta, ejecuta:

```bash
python examples\ejemplo_1_carpeta_placeholders.py
```

Deberías ver:

```
✅ Carpeta creada: DUANY BARO MENÉNDEZ
📁 Archivo subido: imagen1.png
📁 Archivo subido: imagen2.png
📁 Archivo subido: foto1.png
📁 Archivo subido: foto2.png
✅ Proceso completado: 4 archivos subidos
```

## 🔍 Cómo encontrar el email de la Service Account

### Método 1: Desde el archivo JSON

```bash
type light-height-drive-235716-82ec9163785a.json | findstr client_email
```

### Método 2: Desde Google Cloud Console

1. Ve a https://console.cloud.google.com
2. IAM & Admin → Service Accounts
3. Copia el email de tu Service Account

## ⚠️ Importante

- La Service Account necesita permisos de **Editor** en la carpeta
- No es necesario compartir cada subcarpeta, solo la carpeta raíz
- Los archivos se crearán en nombre de la Service Account
