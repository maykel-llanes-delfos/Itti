"""EJEMPLO 6: Procesar clientes desde Excel y crear carpetas"""

from config import AppConfig
from services import GoogleAuthService, GoogleDriveService
from utils import PlaceholderGenerator


def ejemplo_6_procesar_excel_clientes():
    """
    EJEMPLO 6: Lee Excel con nombres de clientes y crea carpetas
    - Lee nombres de clientes desde Excel
    - Detecta duplicados automáticamente
    - Verifica si la carpeta ya existe antes de crearla
    - Usa cache para optimizar búsquedas
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 6: Procesar clientes desde Excel")
    print("=" * 60)

    config = AppConfig()

    # Autenticación
    auth_service = GoogleAuthService(config)
    drive_creds = auth_service.get_credentials(for_service="drive")
    drive_service = GoogleDriveService(drive_creds, config)

    # Paso 1: Crear un Excel de ejemplo con clientes
    print("\n📝 Creando Excel de ejemplo con clientes...")

    import pandas as pd
    import io
    from models import ArchivoCliente

    # Datos de ejemplo con clientes repetidos
    datos_clientes = pd.DataFrame(
        {
            "ID": range(1, 11),
            "Nombre": [
                "JUAN PEREZ LOPEZ",
                "MARIA GARCIA RODRIGUEZ",
                "JUAN PEREZ LOPEZ",  # Repetido
                "CARLOS MARTINEZ SANCHEZ",
                "MARIA GARCIA RODRIGUEZ",  # Repetido
                "ANA FERNANDEZ GOMEZ",
                "JUAN PEREZ LOPEZ",  # Repetido otra vez
                "LUIS GONZALEZ DIAZ",
                "CARLOS MARTINEZ SANCHEZ",  # Repetido
                "SOFIA RAMIREZ TORRES",
            ],
            "Email": [
                "juan.perez@email.com",
                "maria.garcia@email.com",
                "juan.perez@email.com",
                "carlos.martinez@email.com",
                "maria.garcia@email.com",
                "ana.fernandez@email.com",
                "juan.perez@email.com",
                "luis.gonzalez@email.com",
                "carlos.martinez@email.com",
                "sofia.ramirez@email.com",
            ],
            "Telefono": [
                "123456789",
                "987654321",
                "123456789",
                "555666777",
                "987654321",
                "111222333",
                "123456789",
                "444555666",
                "555666777",
                "777888999",
            ],
        }
    )

    # Crear Excel en memoria
    excel_bytes = io.BytesIO()
    datos_clientes.to_excel(excel_bytes, index=False, sheet_name="Clientes")
    excel_bytes.seek(0)

    archivo_excel = ArchivoCliente(
        contenido_bytes=excel_bytes.read(),
        nombre_destino="clientes_ejemplo.xlsx",
        mime_type="application/vnd.openxmlformats-officedocument."
        "spreadsheetml.sheet",
    )

    # Subir Excel a Drive
    folder_id = config.drive_root_folder_id or "ID_DE_TU_CARPETA"
    file_id = drive_service.subir_archivo(archivo_excel, folder_id)
    print(f"✅ Excel subido con ID: {file_id}")

    # Paso 2: Leer el Excel desde Drive
    print("\n📖 Leyendo Excel desde Drive...")
    excel_data = drive_service.leer_excel_desde_drive(file_id)

    print(f"   Hojas: {excel_data.sheet_names}")
    print(f"   Total registros: {sum(len(rows) for rows in excel_data.data.values())}")

    # Mostrar clientes encontrados
    print("\n📋 Clientes en el Excel:")
    for sheet_name, rows in excel_data.data.items():
        nombres = [row.get("Nombre") for row in rows if row.get("Nombre")]
        print(f"   Hoja '{sheet_name}': {len(nombres)} registros")
        print(f"   Clientes únicos: {len(set(nombres))}")

    # Paso 3: Procesar clientes y crear carpetas
    print("\n" + "=" * 60)
    print("PROCESANDO CLIENTES Y CREANDO CARPETAS")
    print("=" * 60)

    carpetas_clientes = drive_service.procesar_clientes_desde_excel(
        excel_data=excel_data,
        columna_nombre="Nombre",
        crear_carpetas=True,
        parent_id=folder_id,
    )

    # Mostrar resultados
    print("\n" + "=" * 60)
    print("RESUMEN DE CARPETAS CREADAS")
    print("=" * 60)

    for nombre, folder_id in sorted(carpetas_clientes.items()):
        print(f"✅ {nombre}")
        print(f"   ID: {folder_id}")

    print(f"\n📊 ESTADÍSTICAS:")
    print(f"   Total registros en Excel: 10")
    print(f"   Clientes únicos: {len(carpetas_clientes)}")
    print(f"   Carpetas procesadas: {len(carpetas_clientes)}")

    print("\n✅ PROCESO COMPLETADO")
    print("\n💡 NOTA:")
    print("   - Si ejecutas este ejemplo otra vez, NO creará carpetas duplicadas")
    print("   - Detectará las carpetas existentes y las reutilizará")


if __name__ == "__main__":
    ejemplo_6_procesar_excel_clientes()
