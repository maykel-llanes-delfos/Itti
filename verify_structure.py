"""Script para verificar que la estructura del proyecto es correcta"""

import sys
from pathlib import Path


def verificar_estructura():
    """Verifica que todos los archivos necesarios existen"""

    archivos_requeridos = [
        # Config
        "config/__init__.py",
        "config/settings.py",
        # Models
        "models/__init__.py",
        "models/schemas.py",
        # Services
        "services/__init__.py",
        "services/auth.py",
        "services/drive.py",
        "services/gmail.py",
        # Jobs
        "jobs/__init__.py",
        "jobs/email_processor.py",
        "jobs/drive_monitor.py",
        # Utils
        "utils/__init__.py",
        "utils/placeholder.py",
        "utils/callbacks.py",
        # Examples
        "examples/__init__.py",
        "examples/ejemplo_1_carpeta_placeholders.py",
        "examples/ejemplo_2_email_a_drive.py",
        "examples/ejemplo_3_monitorear_validar.py",
        "examples/ejemplo_4_leer_actualizar_excel.py",
        "examples/ejemplo_5_flujo_completo.py",
        # Docs
        "README.md",
        "MIGRATION_GUIDE.md",
        "PROYECTO_REFACTORIZADO.md",
        # Main
        "main_refactored.py",
    ]

    print("🔍 Verificando estructura del proyecto...\n")

    errores = []
    for archivo in archivos_requeridos:
        path = Path(archivo)
        if path.exists():
            print(f"✅ {archivo}")
        else:
            print(f"❌ {archivo} - NO ENCONTRADO")
            errores.append(archivo)

    print("\n" + "=" * 60)

    if errores:
        print(f"\n❌ Faltan {len(errores)} archivos:")
        for error in errores:
            print(f"   - {error}")
        return False
    else:
        print("\n✅ Todos los archivos están presentes")
        print("\n🎉 Estructura del proyecto verificada correctamente")
        return True


def verificar_imports():
    """Verifica que los imports funcionan"""

    print("\n" + "=" * 60)
    print("🔍 Verificando imports...\n")

    try:
        from config import AppConfig, AuthMode, GoogleScopes

        print("✅ config imports OK")
    except Exception as e:
        print(f"❌ config imports FAILED: {e}")
        return False

    try:
        from models import (
            Cliente,
            ArchivoCliente,
            EmailMessage,
            DriveFileChange,
            ExcelData,
        )

        print("✅ models imports OK")
    except Exception as e:
        print(f"❌ models imports FAILED: {e}")
        return False

    try:
        from services import GoogleAuthService, GoogleDriveService, GmailService

        print("✅ services imports OK")
    except Exception as e:
        print(f"❌ services imports FAILED: {e}")
        return False

    try:
        from jobs import EmailProcessorJob, DriveMonitorJob

        print("✅ jobs imports OK")
    except Exception as e:
        print(f"❌ jobs imports FAILED: {e}")
        return False

    try:
        from utils import PlaceholderGenerator

        print("✅ utils imports OK")
    except Exception as e:
        print(f"❌ utils imports FAILED: {e}")
        return False

    print("\n✅ Todos los imports funcionan correctamente")
    return True


if __name__ == "__main__":
    print(
        """
╔════════════════════════════════════════════════════════════════╗
║   Verificación de Estructura del Proyecto                     ║
╚════════════════════════════════════════════════════════════════╝
    """
    )

    estructura_ok = verificar_estructura()
    imports_ok = verificar_imports()

    print("\n" + "=" * 60)
    print("\n📊 RESUMEN:")
    print(f"   Estructura: {'✅ OK' if estructura_ok else '❌ ERROR'}")
    print(f"   Imports:    {'✅ OK' if imports_ok else '❌ ERROR'}")

    if estructura_ok and imports_ok:
        print("\n🎉 ¡Proyecto listo para usar!")
        print("\n📚 Próximos pasos:")
        print("   1. Configura tu .env")
        print("   2. Ejecuta: python examples/ejemplo_1_carpeta_placeholders.py")
        sys.exit(0)
    else:
        print("\n❌ Hay problemas que resolver")
        sys.exit(1)
