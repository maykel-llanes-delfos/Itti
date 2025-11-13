"""Job para monitorear cambios en archivos Excel en Drive"""

import time
from typing import Optional, List
from datetime import datetime

from config.settings import AppConfig
from models.schemas import ExcelData
from services.drive import GoogleDriveService


class DriveMonitorJob:
    """Job para monitorear cambios en archivos Excel en Drive"""

    def __init__(self, drive_service: GoogleDriveService, config: AppConfig):
        self.drive_service = drive_service
        self.config = config
        self.last_check: Optional[datetime] = None

    def procesar_cambios(
        self, folder_id: str, callback_on_change: Optional[callable] = None
    ) -> List[ExcelData]:
        """
        Detecta y procesa cambios en archivos Excel

        Args:
            folder_id: ID de la carpeta a monitorear
            callback_on_change: Función a ejecutar cuando hay cambios
                                Debe aceptar ExcelData como parámetro

        Returns:
            Lista de archivos Excel modificados
        """
        print(f"\n📊 Monitoreando cambios en Excel " f"(Carpeta: {folder_id})...")

        cambios = self.drive_service.listar_archivos_excel(folder_id, self.last_check)

        if not cambios:
            print("  No hay cambios")
            self.last_check = datetime.now()
            return []

        print(f"  ✨ Detectados {len(cambios)} cambios")

        excel_data_list = []

        for cambio in cambios:
            print(f"\n  📝 Archivo modificado: {cambio.file_name}")
            print(f"     ID: {cambio.file_id}")
            print(f"     Modificado: {cambio.modified_time}")
            print(f"     Link: {cambio.web_view_link}")

            try:
                # Leer Excel desde Drive
                excel_data = self.drive_service.leer_excel_desde_drive(cambio.file_id)
                excel_data_list.append(excel_data)

                # Ejecutar callback si existe
                if callback_on_change:
                    print("     ⚡ Ejecutando callback personalizado...")
                    callback_on_change(excel_data)

            except Exception as e:
                print(f"     ❌ Error procesando Excel: {e}")

        self.last_check = datetime.now()
        return excel_data_list

    def ejecutar_loop(
        self, folder_id: str, callback_on_change: Optional[callable] = None
    ):
        """Ejecuta el job en loop continuo"""
        print("🚀 Iniciando DriveMonitorJob...")
        print(f"   Intervalo: {self.config.drive_check_interval}s")

        while True:
            try:
                self.procesar_cambios(folder_id, callback_on_change)
            except Exception as e:
                print(f"❌ Error monitoreando cambios: {e}")

            time.sleep(self.config.drive_check_interval)
