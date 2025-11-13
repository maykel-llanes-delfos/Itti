"""EJEMPLO 4: Leer Excel desde Drive, modificar y actualizar"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd

from config import AppConfig
from services import GoogleAuthService, GoogleDriveService
from utils import PlaceholderGenerator


def ejemplo_4_leer_y_actualizar_excel():
    """
    EJEMPLO 4: Leer Excel desde Drive, modificar y actualizar
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 4: Leer y actualizar Excel en Drive")
    print("=" * 60)

    config = AppConfig()

    # Autenticación
    auth_service = GoogleAuthService(config)
    drive_creds = auth_service.get_credentials(for_service="drive")
    drive_service = GoogleDriveService(drive_creds, config)

    # Primero, crear un Excel de prueba
    print("\n📝 Creando Excel de prueba...")
    excel_placeholder = PlaceholderGenerator.crear_excel_placeholder("test_excel.xlsx")

    folder_id = config.drive_root_folder_id or "ID_DE_TU_CARPETA"
    file_id = drive_service.subir_archivo(excel_placeholder, folder_id)

    print(f"   Excel creado con ID: {file_id}")

    # Leer el Excel
    print("\n📖 Leyendo Excel desde Drive...")
    excel_data = drive_service.leer_excel_desde_drive(file_id)

    print(f"   Hojas encontradas: {excel_data.sheet_names}")
    print(f"   Total filas: " f"{sum(len(rows) for rows in excel_data.data.values())}")

    # Modificar datos
    print("\n✏️  Modificando datos...")
    for sheet_name, rows in excel_data.data.items():
        df = pd.DataFrame(rows)

        # Ejemplo: Agregar una nueva columna
        df["Total"] = df["Cantidad"] * df["Precio"]

        # Ejemplo: Agregar una fila resumen
        resumen = pd.DataFrame(
            [
                {
                    "ID": "TOTAL",
                    "Nombre": "",
                    "Cantidad": df["Cantidad"].sum(),
                    "Precio": df["Precio"].mean(),
                    "Total": df["Total"].sum(),
                }
            ]
        )

        df = pd.concat([df, resumen], ignore_index=True)

        # Actualizar en Drive
        print(f"\n💾 Actualizando hoja '{sheet_name}' en Drive...")
        drive_service.actualizar_excel_en_drive(
            file_id=file_id, dataframes={sheet_name: df}
        )

    print("\n✅ Excel actualizado correctamente")

    # Verificar cambios
    print("\n🔍 Verificando cambios...")
    excel_data_updated = drive_service.leer_excel_desde_drive(file_id)

    for sheet_name, rows in excel_data_updated.data.items():
        df = pd.DataFrame(rows)
        print(f"\n  📋 Hoja '{sheet_name}':")
        print(f"     Columnas: {list(df.columns)}")
        print(f"     Filas: {len(df)}")
        if "Total" in df.columns:
            print("     ✅ Nueva columna 'Total' agregada")


if __name__ == "__main__":
    ejemplo_4_leer_y_actualizar_excel()
