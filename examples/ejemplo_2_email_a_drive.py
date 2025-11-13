"""EJEMPLO 2: Job que procesa correos y sube Excel a Drive"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import AppConfig
from services import GoogleAuthService, GoogleDriveService, GmailService
from jobs import EmailProcessorJob


def ejemplo_2_job_email_a_drive():
    """
    EJEMPLO 2: Job que procesa correos y sube Excel a Drive
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 2: Procesar correos y subir a Drive")
    print("=" * 60)

    config = AppConfig()

    # Autenticación
    auth_service = GoogleAuthService(config)

    drive_creds = auth_service.get_credentials(for_service="drive")
    drive_service = GoogleDriveService(drive_creds, config)

    try:
        gmail_creds = auth_service.get_credentials(for_service="gmail")
        gmail_service = GmailService(gmail_creds, config)
    except Exception as e:
        print(f"❌ Gmail service no disponible: {e}")
        return

    # Crear job
    job = EmailProcessorJob(gmail_service, drive_service, config)

    # Opción 1: Ejecutar una vez
    resultados = job.procesar_correos_nuevos(
        guardar_local=True,
        subir_a_drive=True,
        folder_id_drive=config.drive_root_folder_id,
    )

    print(f"\n✅ Procesados {len(resultados)} correos")

    for correo, file_ids in resultados:
        print(f"\n  📧 {correo.subject}")
        print(f"     Archivos en Drive: {len(file_ids)}")
        for file_id in file_ids:
            print(f"       - {file_id}")

    # Opción 2: Loop continuo (descomentar para usar)
    # job.ejecutar_loop(
    #     guardar_local=True,
    #     subir_a_drive=True,
    #     folder_id_drive=config.drive_root_folder_id
    # )


if __name__ == "__main__":
    ejemplo_2_job_email_a_drive()
