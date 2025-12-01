"""EJEMPLO 8: Job automatizado que monitorea Excel y crea carpetas"""

from config import AppConfig
from services import GoogleAuthService, GoogleDriveService
from jobs import ExcelToFoldersJob


def callback_clientes_nuevos(carpetas_nuevas):
    """
    Callback que se ejecuta cuando se detectan clientes nuevos

    Args:
        carpetas_nuevas: Dict {nombre_cliente: folder_id}
    """
    print("\n🎉 ¡CLIENTES NUEVOS DETECTADOS!")
    print("=" * 50)

    for nombre, folder_id in carpetas_nuevas.items():
        print(f"📁 {nombre}")
        print(f"   ID: {folder_id}")
        print(f"   Link: https://drive.google.com/drive/folders/{folder_id}")

    # Aquí puedes agregar lógica adicional:
    # - Enviar notificación por email
    # - Registrar en base de datos
    # - Crear archivos iniciales en la carpeta
    # - etc.


def ejemplo_8_job_automatico():
    """
    EJEMPLO 8: Job que monitorea Excel y crea carpetas automáticamente

    Este job:
    1. Monitorea una carpeta de Drive buscando Excel nuevos/modificados
    2. Lee los nombres de clientes del Excel
    3. Crea carpetas automáticamente para clientes nuevos
    4. Evita duplicados (no crea carpetas que ya existen)
    5. Ejecuta un callback cuando detecta clientes nuevos
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 8: Job automatizado Excel → Carpetas")
    print("=" * 60)

    config = AppConfig()

    # Autenticación
    auth_service = GoogleAuthService(config)
    drive_creds = auth_service.get_credentials(for_service="drive")
    drive_service = GoogleDriveService(drive_creds, config)

    # Crear job
    job = ExcelToFoldersJob(drive_service, config)

    # Configuración
    folder_id = config.drive_root_folder_id or "ID_DE_TU_CARPETA"
    columna_nombre = "Nombre"  # Ajusta según tu Excel

    print(f"\n⚙️  CONFIGURACIÓN:")
    print(f"   Carpeta monitoreada: {folder_id}")
    print(f"   Columna de nombres: {columna_nombre}")
    print(f"   Intervalo de chequeo: {config.drive_check_interval}s")

    print("\n📋 FUNCIONAMIENTO:")
    print("   1. Monitorea Excel en la carpeta configurada")
    print("   2. Detecta archivos nuevos o modificados")
    print("   3. Lee nombres de clientes")
    print("   4. Crea carpetas (solo si no existen)")
    print("   5. Ejecuta callback para clientes nuevos")

    print("\n🔍 OPCIONES:")
    print("   [1] Ejecutar una vez (chequear ahora)")
    print("   [2] Ejecutar en loop continuo (monitoreo permanente)")
    print("   [3] Ver estadísticas")

    opcion = input("\nSelecciona una opción (1-3): ").strip()

    if opcion == "1":
        # Ejecutar una vez
        print("\n🔍 Ejecutando chequeo único...")
        carpetas_nuevas = job.procesar_excel_nuevos(
            folder_id=folder_id, columna_nombre=columna_nombre, crear_carpetas=True
        )

        if carpetas_nuevas:
            callback_clientes_nuevos(carpetas_nuevas)

        # Mostrar estadísticas
        stats = job.obtener_estadisticas()
        print(f"\n📊 ESTADÍSTICAS:")
        print(f"   Total clientes: {stats['total_clientes']}")
        print(f"   Última revisión: {stats['ultima_revision']}")

    elif opcion == "2":
        # Loop continuo
        print("\n🔄 Iniciando monitoreo continuo...")
        print("   (Presiona Ctrl+C para detener)")

        try:
            job.ejecutar_loop(
                folder_id=folder_id,
                columna_nombre=columna_nombre,
                crear_carpetas=True,
                callback_on_new=callback_clientes_nuevos,
            )
        except KeyboardInterrupt:
            print("\n\n⏹️  Job detenido por el usuario")

            # Mostrar estadísticas finales
            stats = job.obtener_estadisticas()
            print(f"\n📊 ESTADÍSTICAS FINALES:")
            print(f"   Total clientes procesados: {stats['total_clientes']}")
            print(f"   Última revisión: {stats['ultima_revision']}")

    elif opcion == "3":
        # Ver estadísticas
        stats = job.obtener_estadisticas()
        print(f"\n📊 ESTADÍSTICAS:")
        print(f"   Total clientes: {stats['total_clientes']}")
        print(f"   Última revisión: {stats['ultima_revision']}")

        if stats["clientes"]:
            print(f"\n   Clientes procesados:")
            for i, nombre in enumerate(sorted(stats["clientes"]), 1):
                print(f"      {i}. {nombre}")

    else:
        print("\n❌ Opción inválida")


if __name__ == "__main__":
    ejemplo_8_job_automatico()
