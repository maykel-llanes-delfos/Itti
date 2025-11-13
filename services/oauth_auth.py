"""Servicio de autenticación OAuth para cuentas personales"""

import os
import pickle
from typing import Literal
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from config.settings import GoogleScopes


class GoogleOAuthService:
    """Servicio de autenticación OAuth para cuentas personales"""

    def __init__(self):
        self.scopes = [
            GoogleScopes.DRIVE_FULL,
            GoogleScopes.GMAIL_READONLY,
            GoogleScopes.GMAIL_MODIFY,
        ]
        self.credentials_file = "credentials.json"
        self.token_file = "token.pickle"

    def get_credentials(self, for_service: Literal["drive", "gmail"] = "drive"):
        """
        Obtiene credenciales OAuth

        Args:
            for_service: "drive" o "gmail"

        Returns:
            Credenciales OAuth configuradas
        """
        creds = None

        # Cargar token existente
        if os.path.exists(self.token_file):
            with open(self.token_file, "rb") as token:
                creds = pickle.load(token)

        # Si no hay credenciales válidas, obtener nuevas
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("🔄 Refrescando token OAuth...")
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(
                        f"Archivo de credenciales OAuth no encontrado: "
                        f"{self.credentials_file}\n"
                        f"Descárgalo desde Google Cloud Console > "
                        f"Credentials > OAuth 2.0 Client ID"
                    )

                print("🔐 Iniciando flujo de autenticación OAuth...")
                print("Se abrirá tu navegador para autorizar la aplicación")

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.scopes
                )
                creds = flow.run_local_server(port=0)

            # Guardar credenciales para la próxima vez
            with open(self.token_file, "wb") as token:
                pickle.dump(creds, token)

        print("✅ Autenticación OAuth completada")
        return creds

    def revoke_credentials(self):
        """Revoca las credenciales actuales"""
        if os.path.exists(self.token_file):
            os.remove(self.token_file)
            print("🗑️ Credenciales OAuth eliminadas")
        else:
            print("ℹ️ No hay credenciales para eliminar")

    def check_credentials_file(self):
        """Verifica si el archivo de credenciales existe"""
        if os.path.exists(self.credentials_file):
            print(f"✅ Archivo de credenciales encontrado: {self.credentials_file}")
            return True
        else:
            print(f"❌ Archivo de credenciales no encontrado: {self.credentials_file}")
            print("\n📋 PASOS PARA OBTENER CREDENCIALES OAUTH:")
            print("1. Ve a Google Cloud Console: https://console.cloud.google.com")
            print("2. Selecciona tu proyecto")
            print("3. Ve a APIs & Services → Credentials")
            print("4. Click en + CREATE CREDENTIALS → OAuth 2.0 Client ID")
            print("5. Application type: Desktop application")
            print("6. Descarga el JSON como 'credentials.json'")
            return False
