"""
Sistema de Gestión de Google Drive y Gmail con Service Accounts
Versión modular y organizada

Requisitos:
pip install google-api-python-client google-auth pydantic openpyxl pandas
"""

if __name__ == "__main__":
    print(
        """
╔════════════════════════════════════════════════════════════════╗
║   Sistema de Gestión Google Drive y Gmail                     ║
║   Con Service Accounts y Pydantic                             ║
╚════════════════════════════════════════════════════════════════╝

📚 EJEMPLOS DISPONIBLES:

1. python examples/ejemplo_1_carpeta_placeholders.py
   - Crea carpeta de cliente con 4 archivos placeholder

2. python examples/ejemplo_2_email_a_drive.py
   - Procesa correos y sube Excel adjuntos a Drive

3. python examples/ejemplo_3_monitorear_validar.py
   - Monitorea cambios en Excel y ejecuta validaciones

4. python examples/ejemplo_4_leer_actualizar_excel.py
   - Lee Excel desde Drive, modifica y actualiza

5. python examples/ejemplo_5_flujo_completo.py
   - Flujo completo integrado: Email -> Drive -> Monitor

⚙️  CONFIGURACIÓN:
   - Edita .env con tus credenciales
   - Coloca service-account.json en la raíz
   - Configura DRIVE_ROOT_FOLDER_ID y filtros Gmail

📁 ESTRUCTURA DEL PROYECTO:
   config/          - Configuración y settings
   models/          - Modelos Pydantic
   services/        - Servicios de Google (Drive, Gmail, Auth)
   jobs/            - Jobs automatizados (Email, Monitor)
   utils/           - Utilidades (Placeholders, Callbacks)
   examples/        - Ejemplos de uso

🚀 Ejecuta un ejemplo usando el comando correspondiente arriba
    """
    )
