"""Servicio de autenticación con Service Accounts y OAuth"""

import os
from typing import Literal
from google.oauth2 import service_account

from config.settings import AppConfig, AuthMode, GoogleScopes


class GoogleAuthService:
    """Servicio de autenticación con Service Accounts"""

    def __init__(self, config: AppConfig):
        self.config = config
        self.scopes = [
            GoogleScopes.DRIVE_FULL,
            GoogleScopes.GMAIL_READONLY,
            GoogleScopes.GMAIL_MODIFY,
        ]

    def get_credentials(self, for_service: Literal["drive", "gmail"] = "drive"):
        """
        Obtiene credenciales (OAuth si está disponible, sino Service Account)

        Args:
            for_service: "drive" o "gmail"

        Returns:
            Credenciales configuradas
        """
        # Si existe credentials.json, usar OAuth
        if os.path.exists("credentials.json"):
            print("🔍 Detectado credentials.json, usando OAuth...")
            from services.oauth_auth import GoogleOAuthService

            oauth_service = GoogleOAuthService()
            return oauth_service.get_credentials(for_service)

        # Sino, usar Service Account
        print("🔍 Usando Service Account...")
        return self._get_service_account_credentials(for_service)

    def _get_service_account_credentials(
        self, for_service: Literal["drive", "gmail"] = "drive"
    ):
        """
        Obtiene credenciales de Service Account (método interno)
        """
        if not os.path.exists(self.config.service_account_file):
            raise FileNotFoundError(
                f"Archivo de service account no encontrado: "
                f"{self.config.service_account_file}"
            )

        # Cargar credenciales base
        credentials = service_account.Credentials.from_service_account_file(
            self.config.service_account_file, scopes=self.scopes
        )

        # Para Workspace con domain-wide delegation
        if self.config.auth_mode == AuthMode.WORKSPACE:
            if not self.config.delegated_user_email:
                raise ValueError(
                    "Para modo WORKSPACE debes configurar DELEGATED_USER_EMAIL"
                )

            # Delegar credenciales al usuario
            credentials = credentials.with_subject(self.config.delegated_user_email)
            print(f"🔐 Usando delegación para: " f"{self.config.delegated_user_email}")
        else:
            print("🔐 Usando Service Account en modo PERSONAL")

        return credentials
