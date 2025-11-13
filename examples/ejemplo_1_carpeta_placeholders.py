"""EJEMPLO 1: Crear carpeta de cliente con archivos placeholder"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import AppConfig
from models import Cliente
from services import GoogleAuthService, GoogleDriveService
from utils import PlaceholderGenerator


def ejemplo_1_crear_carpeta_con_placeholders():
    """
    EJEMPLO 1: Crear carpeta de cliente con archivos placeholder
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 1: Crear carpeta con 4 archivos placeholder")
    print("=" * 60)

    config = AppConfig()

    # Autenticación
    auth_service = GoogleAuthService(config)
    drive_creds = auth_service.get_credentials(for_service="drive")
    drive_service = GoogleDriveService(drive_creds, config)

    # Datos del cliente (pueden venir de cualquier fuente)
    cliente = Cliente(nombre="DUANY", apellido1="BARO", apellido2="MENÉNDEZ")

    # Crear 4 archivos placeholder (2 imágenes + 2 fotos)
    print("\n📦 Generando archivos placeholder...")
    archivos = [
        PlaceholderGenerator.crear_imagen_placeholder("imagen1.png", color="blue"),
        PlaceholderGenerator.crear_imagen_placeholder("imagen2.png", color="green"),
        PlaceholderGenerator.crear_imagen_placeholder("foto1.png", color="red"),
        PlaceholderGenerator.crear_imagen_placeholder("foto2.png", color="purple"),
    ]

    # Crear carpeta y subir archivos
    folder_id, archivos_subidos = drive_service.crear_carpeta_con_archivos(
        nombre_carpeta=cliente.nombre_carpeta,
        archivos=archivos,
        parent_id=config.drive_root_folder_id,
    )

    print("\n✅ COMPLETADO")
    print(f"   Carpeta ID: {folder_id}")
    print(f"   Archivos: {list(archivos_subidos.keys())}")


if __name__ == "__main__":
    ejemplo_1_crear_carpeta_con_placeholders()
