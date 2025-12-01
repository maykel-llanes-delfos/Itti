"""Job para procesar Excel y crear carpetas de clientes automáticamente"""

import time
from typing import Optional, Dict
from datetime import datetime

from config.settings import AppConfig
from models.schemas import ExcelData
from services.drive import GoogleDriveService


class ExcelToFoldersJob:
    """Job que monitorea Excel y crea carpetas para clientes nuevos"""

    def __init__(self, drive_service: GoogleDriveService, config: AppConfig):
        self.drive_service = drive_service
        self.config = config
        self.last_check: Optional[datetime] = None
        self.clientes_procesados: Dict[str, str] = {}  # {nombre: folder_id}

    def procesar_excel_nuevos(
        self,
        folder_id: str,
        columna_nombre: str = "Nombre",
        crear_carpetas: bool = True,
    ) -> Dict[str, str]:
        """
        Procesa archivos Excel nuevos o modificados

        Args:
            folder_id: ID de la carpeta a monitorear
            columna_nombre: Nombre de la columna con nombres de clientes
            crear_carpetas: Si True, crea carpetas para clientes nuevos

        Returns:
            Diccionario con carpetas procesadas {nombre: folder_id}
        """
        print(f"\n📊 Monitoreando Excel en carpeta: {folder_id}")

        # Buscar archivos Excel modificados
        cambios = self.drive_service.listar_archivos_excel(folder_id, self.last_check)

        if not cambios:
            print("  No hay cambios")
            self.last_check = datetime.now()
            return {}

        print(f"  ✨ Detectados {len(cambios)} archivos Excel modificados")

        carpetas_nuevas = {}

        for cambio in cambios:
            print(f"\n  📝 Procesando: {cambio.file_name}")

            try:
                # Leer Excel
                excel_data = self.drive_service.leer_excel_desde_drive(cambio.file_id)

                # Procesar clientes
                carpetas = self.drive_service.procesar_clientes_desde_excel(
                    excel_data=excel_data,
                    columna_nombre=columna_nombre,
                    crear_carpetas=crear_carpetas,
                    parent_id=self.config.drive_root_folder_id,
                )

                # Detectar clientes nuevos
                for nombre, folder_id in carpetas.items():
                    if nombre not in self.clientes_procesados:
                        print(f"     🆕 Cliente nuevo: {nombre}")
                        carpetas_nuevas[nombre] = folder_id

                    self.clientes_procesados[nombre] = folder_id

            except Exception as e:
                print(f"     ❌ Error procesando Excel: {e}")

        self.last_check = datetime.now()

        if carpetas_nuevas:
            print(f"\n✅ {len(carpetas_nuevas)} carpetas nuevas creadas")
        else:
            print("\n  ℹ️  No hay clientes nuevos")

        return carpetas_nuevas

    def ejecutar_loop(
        self,
        folder_id: str,
        columna_nombre: str = "Nombre",
        crear_carpetas: bool = True,
        callback_on_new: Optional[callable] = None,
    ):
        """
        Ejecuta el job en loop continuo

        Args:
            folder_id: ID de la carpeta a monitorear
            columna_nombre: Nombre de la columna con nombres
            crear_carpetas: Si True, crea carpetas automáticamente
            callback_on_new: Función a ejecutar cuando hay clientes nuevos
        """
        print("🚀 Iniciando ExcelToFoldersJob...")
        print(f"   Carpeta monitoreada: {folder_id}")
        print(f"   Columna de nombres: {columna_nombre}")
        print(f"   Intervalo: {self.config.drive_check_interval}s")

        while True:
            try:
                carpetas_nuevas = self.procesar_excel_nuevos(
                    folder_id=folder_id,
                    columna_nombre=columna_nombre,
                    crear_carpetas=crear_carpetas,
                )

                # Ejecutar callback si hay clientes nuevos
                if carpetas_nuevas and callback_on_new:
                    callback_on_new(carpetas_nuevas)

            except Exception as e:
                print(f"❌ Error en el job: {e}")

            time.sleep(self.config.drive_check_interval)

    def obtener_estadisticas(self) -> Dict:
        """Obtiene estadísticas del job"""
        return {
            "total_clientes": len(self.clientes_procesados),
            "ultima_revision": self.last_check,
            "clientes": list(self.clientes_procesados.keys()),
        }
