from enum import Enum
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class AuthMode(str, Enum):
    """Modo de autenticación"""

    PERSONAL = "personal"  # Service Account para uso personal
    WORKSPACE = "workspace"  # Service Account con domain-wide delegation


class GoogleScopes:
    """Scopes de Google API"""

    DRIVE_FULL = "https://www.googleapis.com/auth/drive"
    GMAIL_READONLY = "https://www.googleapis.com/auth/gmail.readonly"
    GMAIL_MODIFY = "https://www.googleapis.com/auth/gmail.modify"


class AppConfig(BaseSettings):
    """Configuración de la aplicación desde variables de entorno"""

    # Modo de autenticación
    auth_mode: AuthMode = Field(default=AuthMode.PERSONAL)

    # Service Account
    service_account_file: str = Field(
        default="service-account.json", description="Archivo JSON de la service account"
    )

    # Para Workspace con domain-wide delegation
    delegated_user_email: Optional[str] = Field(
        default=None, description="Email del usuario a suplantar (solo para Workspace)"
    )

    # Configuración Gmail
    gmail_filter_subject: Optional[str] = Field(default=None)
    gmail_filter_from: Optional[str] = Field(default=None)
    gmail_filter_label: Optional[str] = Field(default=None)
    gmail_check_interval: int = Field(default=60)

    # Configuración Drive
    drive_root_folder_id: Optional[str] = Field(default=None)
    drive_check_interval: int = Field(default=300)

    # Rutas locales
    local_download_path: str = Field(default="./downloads")
    local_temp_path: str = Field(default="./temp")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
