"""Callbacks personalizados para procesamiento de Excel"""

import pandas as pd
from models.schemas import ExcelData


def ejemplo_callback_validacion(excel_data: ExcelData):
    """
    Ejemplo de callback para validación de datos
    Se ejecuta cada vez que se detecta un cambio en Excel
    """
    print(f"\n🔍 VALIDANDO: {excel_data.file_name}")

    for sheet_name, rows in excel_data.data.items():
        print(f"\n  📋 Hoja: {sheet_name}")
        print(f"     Total filas: {len(rows)}")

        if not rows:
            print("     ⚠️  Hoja vacía")
            continue

        # Ejemplo: Validar que no haya valores nulos en columnas críticas
        columnas_requeridas = ["ID", "Nombre"]  # Ajustar según tu caso

        for col in columnas_requeridas:
            if col in rows[0]:
                valores_nulos = sum(1 for row in rows if not row.get(col))
                if valores_nulos > 0:
                    print(f"     ⚠️  Columna '{col}': " f"{valores_nulos} valores nulos")
                else:
                    print(f"     ✅ Columna '{col}': OK")

        # Ejemplo: Validar rangos numéricos
        if "Precio" in rows[0]:
            precios = [row.get("Precio", 0) for row in rows if row.get("Precio")]
            if precios:
                min_precio = min(precios)
                max_precio = max(precios)
                print(
                    f"     💰 Rango de precios: "
                    f"${min_precio:.2f} - ${max_precio:.2f}"
                )

                if min_precio < 0:
                    print("     ❌ ERROR: Hay precios negativos")


def ejemplo_callback_actualizar_bd(excel_data: ExcelData):
    """
    Ejemplo de callback para actualizar base de datos
    """
    print(f"\n💾 ACTUALIZANDO BASE DE DATOS desde: " f"{excel_data.file_name}")

    # Aquí iría tu código de actualización de BD
    # Ejemplo con SQLAlchemy:
    """
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    engine = create_engine('postgresql://user:pass@localhost/dbname')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    for sheet_name, rows in excel_data.data.items():
        for row in rows:
            # Actualizar o insertar en BD
            registro = MiModelo(**row)
            session.merge(registro)
    
    session.commit()
    """

    print(
        f"     ✅ {sum(len(rows) for rows in excel_data.data.values())} "
        f"registros procesados"
    )


def ejemplo_callback_generar_reporte(excel_data: ExcelData):
    """
    Ejemplo de callback para generar reportes automáticos
    """
    print(f"\n📊 GENERANDO REPORTE desde: {excel_data.file_name}")

    for sheet_name, rows in excel_data.data.items():
        if not rows:
            continue

        # Convertir a DataFrame para análisis
        df = pd.DataFrame(rows)

        print(f"\n  📈 Análisis de '{sheet_name}':")
        print(f"     Total registros: {len(df)}")

        # Estadísticas de columnas numéricas
        numeric_cols = df.select_dtypes(include=["number"]).columns
        if len(numeric_cols) > 0:
            print("\n     Columnas numéricas:")
            for col in numeric_cols:
                print(f"       - {col}:")
                print(f"         Media: {df[col].mean():.2f}")
                print(f"         Suma: {df[col].sum():.2f}")
