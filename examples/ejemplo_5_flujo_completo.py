"""EJEMPLO 5: Flujo completo - Email -> Drive -> Monitor"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import AppConfig
from services import GoogleAuthService, GoogleDriveService, GmailService
from jobs import EmailProcessorJob, DriveMonitorJob
from utils import PlaceholderGenerator
from utils.callbacks import ejemplo_callback_validacion


def ejemplo_5_flujo_completo():
    """
    EJEMPLO 5: Flujo completo - Email -> Drive -> Monitor -> Validación
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 5: Flujo completo integrado")
    print("=" * 60)

    config = AppConfig()

    # Autenticación
    auth_service = GoogleAuthService(config)
    drive_creds = auth_service.get_credentials(for_service="drive")
    drive_service = GoogleDriveService(drive_creds, config)

    try:
        gmail_creds = auth_service.get_credentials(for_service="gmail")
        gmail_service = GmailService(gmail_creds, config)
    except Exception:
        gmail_service = None

    if not gmail_service:
        print("⚠️  Modo sin Gmail - Usando Excel de prueba")

        # Crear Excel de prueba directamente en Drive
        excel_placeholder = PlaceholderGenerator.crear_excel_placeholder(
            "flujo_test.xlsx"
        )
        folder_id = config.drive_root_folder_id or "ID_DE_TU_CARPETA"
        file_id = drive_service.subir_archivo(excel_placeholder, folder_id)
        print(f"✅ Excel de prueba creado: {file_id}")

    else:
        # Paso 1: Procesar correos y subir a Drive
        print("\n📧 PASO 1: Procesar correos...")
        email_job = EmailProcessorJob(gmail_service, drive_service, config)
        resultados = email_job.procesar_correos_nuevos(
            guardar_local=True,
            subir_a_drive=True,
            folder_id_drive=config.drive_root_folder_id,
        )

        if resultados:
            print(f"✅ {len(resultados)} correos procesados")
        else:
            print("ℹ️  No hay correos nuevos")

    # Paso 2: Monitorear cambios
    print("\n📊 PASO 2: Monitorear cambios en Drive...")
    monitor_job = DriveMonitorJob(drive_service, config)

    folder_id = config.drive_root_folder_id or "ID_DE_TU_CARPETA"

    cambios = monitor_job.procesar_cambios(
        folder_id=folder_id, callback_on_change=ejemplo_callback_validacion
    )

    if cambios:
        print(f"✅ {len(cambios)} archivos modificados procesados")
    else:
        print("ℹ️  No hay cambios detectados")

    print("\n✅ FLUJO COMPLETO FINALIZADO")


if __name__ == "__main__":
    ejemplo_5_flujo_completo()
