"""Job para procesar correos entrantes con adjuntos Excel"""

import os
import time
from pathlib import Path
from typing import Optional, List
from datetime import datetime

from config.settings import AppConfig
from models.schemas import EmailMessage, ArchivoCliente
from services.gmail import GmailService
from services.drive import GoogleDriveService


class EmailProcessorJob:
    """Job para procesar correos entrantes con adjuntos Excel"""

    def __init__(
        self,
        gmail_service: GmailService,
        drive_service: GoogleDriveService,
        config: AppConfig,
    ):
        self.gmail_service = gmail_service
        self.drive_service = drive_service
        self.config = config

    def procesar_correos_nuevos(
        self,
        guardar_local: bool = True,
        subir_a_drive: bool = True,
        folder_id_drive: Optional[str] = None,
    ) -> List[tuple[EmailMessage, List[str]]]:
        """
        Procesa correos nuevos y maneja adjuntos Excel

        Args:
            guardar_local: Si True, guarda adjuntos localmente
            subir_a_drive: Si True, sube adjuntos a Drive
            folder_id_drive: ID de carpeta Drive destino

        Returns:
            Lista de tuplas (correo, [file_ids_en_drive])
        """
        print("\n📧 Procesando correos nuevos...")

        correos = self.gmail_service.buscar_correos(unread_only=True)

        if not correos:
            print("  No hay correos nuevos")
            return []

        print(f"  Encontrados {len(correos)} correos nuevos")

        resultados = []

        for correo in correos:
            print(f"\n  📨 Procesando: {correo.subject}")
            print(f"     De: {correo.sender}")
            print(f"     Fecha: {correo.date}")

            excel_attachments = self.gmail_service.extraer_excel_adjuntos(correo)

            if not excel_attachments:
                print("     ⚠️  No se encontraron adjuntos Excel")
                continue

            file_ids = []

            for att in excel_attachments:
                # Guardar localmente
                if guardar_local:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{timestamp}_{att.filename}"
                    destino = os.path.join(self.config.local_download_path, filename)

                    Path(destino).parent.mkdir(parents=True, exist_ok=True)
                    with open(destino, "wb") as f:
                        f.write(att.data)

                    print(f"     💾 Guardado local: {destino}")

                # Subir a Drive
                if subir_a_drive:
                    if not folder_id_drive:
                        folder_id_drive = self.config.drive_root_folder_id

                    if folder_id_drive:
                        archivo = ArchivoCliente(
                            contenido_bytes=att.data,
                            nombre_destino=att.filename,
                            mime_type=att.mime_type,
                        )

                        file_id = self.drive_service.subir_archivo(
                            archivo, folder_id_drive
                        )
                        file_ids.append(file_id)
                    else:
                        print("     ⚠️  No hay folder_id_drive configurado")

            # Marcar como leído
            self.gmail_service.marcar_como_leido(correo.id)

            resultados.append((correo, file_ids))

        print(f"\n✅ Procesados {len(resultados)} correos")
        return resultados

    def ejecutar_loop(
        self,
        guardar_local: bool = True,
        subir_a_drive: bool = True,
        folder_id_drive: Optional[str] = None,
    ):
        """Ejecuta el job en loop continuo"""
        print("🚀 Iniciando EmailProcessorJob...")
        print(f"   Intervalo: {self.config.gmail_check_interval}s")

        while True:
            try:
                self.procesar_correos_nuevos(
                    guardar_local=guardar_local,
                    subir_a_drive=subir_a_drive,
                    folder_id_drive=folder_id_drive,
                )
            except Exception as e:
                print(f"❌ Error procesando correos: {e}")

            time.sleep(self.config.gmail_check_interval)
