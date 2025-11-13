"""Test simple de OAuth - Solo crear carpeta"""

import os
from services.oauth_auth import GoogleOAuthService
from services.drive import GoogleDriveService
from config import AppConfig


def test_oauth_simple():
    """Test simple: solo crear una carpeta"""

    print("🔍 Test OAuth Simple - Solo crear carpeta")
    print("=" * 50)

    # Verificar que existe credentials.json
    if not os.path.exists("credentials.json"):
        print("❌ No se encontró credentials.json")
        print("\n📋 PASOS PARA OBTENER CREDENCIALES:")
        print("1. Ve a: https://console.cloud.google.com")
        print("2. Selecciona tu proyecto: light-height-235716")
        print("3. Ve a APIs & Services → Credentials")
        print("4. + CREATE CREDENTIALS → OAuth 2.0 Client ID")
        print("5. Application type: Desktop application")
        print("6. Descarga como 'credentials.json'")
        return

    try:
        # Configurar OAuth
        oauth_service = GoogleOAuthService()
        credentials = oauth_service.get_credentials()

        # Configurar Drive
        config = AppConfig()
        drive_service = GoogleDriveService(credentials, config)

        # Solo crear carpeta (esto debería funcionar)
        print("\n📁 Creando carpeta de prueba...")
        folder_id = drive_service.crear_carpeta("OAUTH_TEST_SIMPLE")

        print(f"✅ ¡Éxito! Carpeta creada: {folder_id}")
        print("\n🎉 OAuth funciona correctamente")
        print("💡 Ahora puedes ejecutar los ejemplos normalmente")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    test_oauth_simple()
