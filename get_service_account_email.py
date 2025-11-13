"""Script para obtener el email de la Service Account"""

import json
import os


def obtener_email_service_account():
    """Obtiene el email de la service account desde el archivo JSON"""

    # Buscar el archivo en diferentes ubicaciones
    posibles_rutas = [
        "service-account.json",
        "config/service-account.json",
        "./config/service-account.json",
    ]

    service_account_file = None
    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            service_account_file = ruta
            break

    if not service_account_file:
        print("❌ No se encontró el archivo service-account.json")
        print("💡 Buscado en: service-account.json, config/service-account.json")
        print("💡 Asegúrate de que el archivo exista en una de estas ubicaciones")
        return None

    try:
        with open(service_account_file, "r") as f:
            data = json.load(f)

        email = data.get("client_email")
        project_id = data.get("project_id")

        print("📧 INFORMACIÓN DE SERVICE ACCOUNT")
        print("=" * 50)
        print(f"Email: {email}")
        print(f"Proyecto: {project_id}")
        print("=" * 50)

        print("\n🎯 PASOS PARA CONFIGURAR SHARED DRIVE:")
        print("1. Ve a Google Drive: https://drive.google.com")
        print("2. Click en 'Nuevo' → 'Más' → 'Unidad compartida'")
        print("3. Dale un nombre: 'Itti Storage'")
        print("4. Una vez creada, click en ⚙️ → 'Administrar miembros'")
        print("5. Click en 'Agregar miembros'")
        print(f"6. Agrega este email: {email}")
        print("7. Dale permisos de 'Editor'")
        print("8. Copia el ID del Shared Drive de la URL")
        print("9. Actualiza DRIVE_ROOT_FOLDER_ID en tu .env")

        return email

    except Exception as e:
        print(f"❌ Error leyendo el archivo: {e}")
        return None


if __name__ == "__main__":
    print(
        """
╔════════════════════════════════════════════════════════════════╗
║              OBTENER EMAIL DE SERVICE ACCOUNT                 ║
╚════════════════════════════════════════════════════════════════╝
    """
    )

    email = obtener_email_service_account()

    if email:
        print(f"\n✅ Email obtenido: {email}")
        print("\n📋 COPIA ESTE EMAIL PARA AGREGARLO AL SHARED DRIVE")
    else:
        print("\n❌ No se pudo obtener el email")
