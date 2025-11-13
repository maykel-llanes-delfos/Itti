"""Script para configurar OAuth por primera vez"""

from services.oauth_auth import GoogleOAuthService
from config import AppConfig
from services.drive import GoogleDriveService
from utils import PlaceholderGenerator


def setup_oauth():
    """Configura OAuth y hace una prueba básica"""

    print(
        """
╔════════════════════════════════════════════════════════════════╗
║                    CONFIGURACIÓN OAUTH                        ║
╚════════════════════════════════════════════════════════════════╝
    """
    )

    # Verificar archivo de credenciales
    oauth_service = GoogleOAuthService()

    if not oauth_service.check_credentials_file():
        print("\n❌ Primero necesitas descargar credentials.json")
        return False

    try:
        # Obtener credenciales (esto abrirá el navegador)
        print("\n🔐 Obteniendo credenciales OAuth...")
        credentials = oauth_service.get_credentials()

        # Probar con Drive
        print("\n🔍 Probando acceso a Google Drive...")
        config = AppConfig()
        drive_service = GoogleDriveService(credentials, config)

        # Crear carpeta de prueba
        folder_id = drive_service.crear_carpeta("OAUTH_TEST")
        print(f"✅ Carpeta de prueba creada: {folder_id}")

        # Subir archivo de prueba
        print("\n📁 Probando subida de archivo...")
        archivo = PlaceholderGenerator.crear_imagen_placeholder(
            "oauth_test.png", ancho=200, alto=200, color="blue"
        )

        file_id = drive_service.subir_archivo(archivo, folder_id)
        print(f"✅ Archivo de prueba subido: {file_id}")

        print("\n🎉 ¡OAUTH CONFIGURADO CORRECTAMENTE!")
        print("\n✅ Ahora puedes usar los ejemplos:")
        print("   python examples/ejemplo_1_carpeta_placeholders.py")

        # Actualizar .env para usar OAuth
        print("\n⚙️ Actualizando configuración...")
        actualizar_env_para_oauth()

        return True

    except Exception as e:
        print(f"\n❌ Error configurando OAuth: {e}")
        return False


def actualizar_env_para_oauth():
    """Actualiza el .env para indicar que se use OAuth"""

    # Leer .env actual
    with open(".env", "r", encoding="utf-8") as f:
        contenido = f.read()

    # Agregar comentario sobre OAuth
    if "# OAUTH CONFIGURADO" not in contenido:
        oauth_config = """

# ============================================================================
# OAUTH CONFIGURADO
# ============================================================================
# OAuth está configurado y funcionando
# Los ejemplos usarán automáticamente OAuth si credentials.json existe
# Para volver a Service Account, elimina credentials.json y token.pickle
"""

        with open(".env", "a", encoding="utf-8") as f:
            f.write(oauth_config)

        print("✅ Configuración actualizada en .env")


if __name__ == "__main__":
    success = setup_oauth()

    if success:
        print(f"\n📋 ARCHIVOS CREADOS:")
        print(f"   ✅ credentials.json (credenciales OAuth)")
        print(f"   ✅ token.pickle (token de acceso)")
        print(f"\n💡 IMPORTANTE:")
        print(f"   - No subas estos archivos a Git")
        print(f"   - Ya están en .gitignore")
    else:
        print(f"\n❌ Configuración fallida")
        print(f"💡 Revisa las instrucciones en SOLUCION_OAUTH.md")
