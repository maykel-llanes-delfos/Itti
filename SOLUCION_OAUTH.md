# 🚀 Solución Simple: OAuth en lugar de Service Account

## ❌ Problema con Service Accounts

- Service Accounts no pueden subir archivos a Drive personal
- Shared Drives solo existen en Google Workspace (empresarial)
- Tu cuenta personal de Gmail no tiene Shared Drives

## ✅ Solución: OAuth con tu cuenta personal

### Ventajas de OAuth:

- ✅ Funciona con cuentas personales de Gmail
- ✅ Acceso completo a tu Drive personal
- ✅ No necesita Shared Drives
- ✅ Configuración más simple

## 🔧 Implementación

### Paso 1: Crear credenciales OAuth

1. Ve a [Google Cloud Console](https://console.cloud.google.com)
2. Selecciona tu proyecto: `light-height-235716`
3. Ve a **APIs & Services** → **Credentials**
4. Click en **+ CREATE CREDENTIALS** → **OAuth 2.0 Client ID**
5. Si es la primera vez, configura la pantalla de consentimiento:
   - User Type: **External**
   - App name: **Itti Drive Manager**
   - User support email: tu email
   - Developer contact: tu email
6. Vuelve a Credentials → **+ CREATE CREDENTIALS** → **OAuth 2.0 Client ID**
7. Application type: **Desktop application**
8. Name: **Itti Desktop Client**
9. Click **CREATE**
10. **Descarga el JSON** y guárdalo como `credentials.json` en la raíz del proyecto

### Paso 2: Instalar dependencia adicional

```bash
pip install google-auth-oauthlib
```

### Paso 3: Crear servicio OAuth

Voy a crear un nuevo servicio que use OAuth en lugar de Service Account.
