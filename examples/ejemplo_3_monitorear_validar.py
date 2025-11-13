"""EJEMPLO 3: Monitorear cambios en Excel y ejecutar validación"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import AppConfig
from services import GoogleAuthService, GoogleDriveService
from jobs import DriveMonitorJob
from utils.callbacks import ejemplo_callback_validacion


def ejemplo_3_monitorear_y_validar():
    """
    EJEMPLO 3: Monitorear cambios en Excel y ejecutar validación
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 3: Monitorear cambios con validación automática")
    print("=" * 60)

    config = AppConfig()

    # Autenticación
    auth_service = GoogleAuthService(config)
    drive_creds = auth_service.get_credentials(for_service="drive")
    drive_service = GoogleDriveService(drive_creds, config)

    # Crear job de monitoreo
    job = DriveMonitorJob(drive_service, config)

    # ID de carpeta a monitorear
    folder_id = config.drive_root_folder_id or "ID_DE_TU_CARPETA"

    print(f"\n📂 Monitoreando carpeta: {folder_id}")

    # Opción 1: Chequear una vez con callback de validación
    cambios = job.procesar_cambios(
        folder_id=folder_id, callback_on_change=ejemplo_callback_validacion
    )

    print(f"\n✅ Detectados {len(cambios)} cambios")

    # Opción 2: Loop continuo con callback (descomentar para usar)
    # job.ejecutar_loop(
    #     folder_id=folder_id,
    #     callback_on_change=ejemplo_callback_validacion
    # )


if __name__ == "__main__":
    ejemplo_3_monitorear_y_validar()
