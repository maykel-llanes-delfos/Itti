"""Script para verificar que el Shared Drive funciona correctamente"""

from config import AppConfig
from services import GoogleAuthService, GoogleDriveService
from utils import PlaceholderGenerator


def verificar_shared_drive():
    """Verifica que el Shared Drive esté configurado correctamente"""

    print(
        """
╔════════════════════════════════════════════════════════════════╗
║              VERIFICAR CONFIGURACIÓN SHARED DRIVE             ║
╚════════════════════════════════════════════════════════════════╝
    """
    )

    try:
        # Cargar configuración
        config = AppConfig()

        if not config.drive_root_folder_id:
            print("❌ DRIVE_ROOT_FOLDER_ID no está configurado en .env")
            print("💡 Actualiza tu .env con el ID del Shared Drive")
            return False

        if config.drive_root_folder_id == "TU_SHARED_DRIVE_ID_AQUI":
            print("❌ DRIVE_ROOT_FOLDER_ID no ha sido actualizado")
            print("💡 Reemplaza 'TU_SHARED_DRIVE_ID_AQUI' con el ID real")
            return False

        print(f"📂 Usando Shared Drive ID: {config.drive_root_folder_id}")

        # Autenticación
        auth = GoogleAuthService(config)
        drive = GoogleDriveService(auth.get_credentials(), config)

        print("\n🔍 PASO 1: Verificando acceso al Shared Drive...")

        # Intentar crear una carpeta de prueba
        try:
            folder_id = drive.crear_carpeta("TEST_VERIFICACION")
            print(f"✅ Carpeta de prueba creada: {folder_id}")
        except Exception as e:
            print(f"❌ Error creando carpeta: {e}")
            print("\n💡 POSIBLES SOLUCIONES:")
            print("   1. Verifica que el ID del Shared Drive sea correcto")
            print(
                "   2. Asegúrate de haber agregado la Service Account al Shared Drive"
            )
            print("   3. Verifica que la Service Account tenga permisos de 'Editor'")
            return False

        print("\n🔍 PASO 2: Verificando subida de archivos...")

        # Intentar subir un archivo pequeño
        try:
            archivo = PlaceholderGenerator.crear_imagen_placeholder(
                "test_verificacion.png", ancho=100, alto=100, color="green"
            )
            file_id = drive.subir_archivo(archivo, folder_id)
            print(f"✅ Archivo de prueba subido: {file_id}")
        except Exception as e:
            print(f"❌ Error subiendo archivo: {e}")
            return False

        print("\n🎉 ¡SHARED DRIVE CONFIGURADO CORRECTAMENTE!")
        print("\n✅ Ahora puedes ejecutar los ejemplos:")
        print("   python examples/ejemplo_1_carpeta_placeholders.py")

        # Limpiar archivos de prueba
        print("\n🧹 Limpiando archivos de prueba...")
        try:
            # Aquí podrías agregar código para eliminar los archivos de prueba
            # Por ahora los dejamos para que veas que funcionó
            print("💡 Puedes eliminar manualmente la carpeta 'TEST_VERIFICACION'")
        except:
            pass

        return True

    except Exception as e:
        print(f"❌ Error general: {e}")
        return False


def mostrar_instrucciones():
    """Muestra las instrucciones para configurar el Shared Drive"""

    print(
        """
📋 INSTRUCCIONES PARA CONFIGURAR SHARED DRIVE:

1. 🌐 Ve a Google Drive: https://drive.google.com

2. 📁 Crear Shared Drive:
   • Click en "Nuevo" → "Más" → "Unidad compartida"
   • Nombre: "Itti Storage" (o el que prefieras)
   • Click en "Crear"

3. 👥 Agregar Service Account:
   • Abre el Shared Drive creado
   • Click en ⚙️ → "Administrar miembros"
   • Click en "Agregar miembros"
   • Agrega: drive-api-user@light-height-235716.iam.gserviceaccount.com
   • Permisos: "Editor"
   • Click en "Enviar"

4. 🔗 Obtener ID:
   • Copia el ID de la URL del Shared Drive
   • Ejemplo: https://drive.google.com/drive/folders/1ABC123xyz456
   • El ID sería: 1ABC123xyz456

5. ⚙️ Actualizar .env:
   • Abre tu archivo .env
   • Cambia: DRIVE_ROOT_FOLDER_ID=tu_id_aqui

6. ✅ Verificar:
   • Ejecuta: python verificar_shared_drive.py
    """
    )


if __name__ == "__main__":
    # Verificar configuración
    if not verificar_shared_drive():
        print("\n" + "=" * 60)
        mostrar_instrucciones()
