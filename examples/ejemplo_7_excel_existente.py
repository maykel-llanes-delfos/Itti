"""EJEMPLO 7: Procesar Excel existente con clientes"""

from config import AppConfig
from services import GoogleAuthService, GoogleDriveService


def ejemplo_7_excel_existente():
    """
    EJEMPLO 7: Procesa un Excel que ya existe en Drive

    USO:
    1. Sube tu Excel a Drive manualmente
    2. Copia el ID del archivo de la URL
    3. Actualiza FILE_ID abajo con tu ID
    4. Ejecuta este script
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 7: Procesar Excel existente")
    print("=" * 60)

    # ⚠️ CONFIGURACIÓN: Actualiza estos valores
    FILE_ID = "TU_FILE_ID_AQUI"  # ID del Excel en Drive
    COLUMNA_NOMBRE = "Nombre"  # Nombre de la columna con nombres

    if FILE_ID == "TU_FILE_ID_AQUI":
        print("\n❌ ERROR: Debes configurar FILE_ID")
        print("\n📋 PASOS:")
        print("1. Sube tu Excel a Google Drive")
        print("2. Abre el archivo en Drive")
        print("3. Copia el ID de la URL:")
        print("   https://drive.google.com/file/d/FILE_ID_AQUI/view")
        print("4. Actualiza FILE_ID en este script")
        return

    config = AppConfig()

    # Autenticación
    auth_service = GoogleAuthService(config)
    drive_creds = auth_service.get_credentials(for_service="drive")
    drive_service = GoogleDriveService(drive_creds, config)

    # Leer Excel desde Drive
    print(f"\n📖 Leyendo Excel desde Drive (ID: {FILE_ID})...")

    try:
        excel_data = drive_service.leer_excel_desde_drive(FILE_ID)
    except Exception as e:
        print(f"❌ Error leyendo Excel: {e}")
        print("\n💡 Verifica que:")
        print("   - El FILE_ID sea correcto")
        print("   - El archivo sea un Excel (.xlsx)")
        print("   - Tengas permisos para acceder al archivo")
        return

    print(f"✅ Excel leído: {excel_data.file_name}")
    print(f"   Hojas: {', '.join(excel_data.sheet_names)}")

    # Mostrar vista previa de los datos
    print("\n📋 Vista previa de los datos:")
    for sheet_name, rows in excel_data.data.items():
        print(f"\n   Hoja: {sheet_name}")
        print(f"   Total filas: {len(rows)}")

        if rows:
            print(f"   Columnas: {', '.join(rows[0].keys())}")

            # Verificar si existe la columna de nombres
            if COLUMNA_NOMBRE not in rows[0]:
                print(f"\n   ⚠️  Columna '{COLUMNA_NOMBRE}' no encontrada")
                print(f"   Columnas disponibles: {', '.join(rows[0].keys())}")
                print(f"\n   💡 Actualiza COLUMNA_NOMBRE en el script")
                return

            # Mostrar primeras 3 filas
            print(f"\n   Primeras filas:")
            for i, row in enumerate(rows[:3], 1):
                nombre = row.get(COLUMNA_NOMBRE, "N/A")
                print(f"      {i}. {nombre}")

    # Procesar clientes
    print("\n" + "=" * 60)
    print("PROCESANDO CLIENTES")
    print("=" * 60)

    carpetas_clientes = drive_service.procesar_clientes_desde_excel(
        excel_data=excel_data,
        columna_nombre=COLUMNA_NOMBRE,
        crear_carpetas=True,
        parent_id=config.drive_root_folder_id,
    )

    # Mostrar resultados
    print("\n" + "=" * 60)
    print("CARPETAS CREADAS/ENCONTRADAS")
    print("=" * 60)

    for i, (nombre, folder_id) in enumerate(sorted(carpetas_clientes.items()), 1):
        print(f"{i}. {nombre}")
        print(f"   ID: {folder_id}")
        print(f"   Link: https://drive.google.com/drive/folders/{folder_id}")

    print(f"\n✅ COMPLETADO: {len(carpetas_clientes)} carpetas procesadas")


if __name__ == "__main__":
    ejemplo_7_excel_existente()
