"""Servicio de Gmail"""

import base64
from typing import Optional, List, Dict, Any
from datetime import datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config.settings import AppConfig
from models.schemas import EmailMessage, EmailAttachment


class GmailService:
    """Servicio para interactuar con Gmail"""

    def __init__(self, credentials, config: AppConfig):
        self.service = build("gmail", "v1", credentials=credentials)
        self.config = config

    def _construir_query(self) -> str:
        """Construye query de búsqueda"""
        queries = ["has:attachment"]

        if self.config.gmail_filter_subject:
            queries.append(f"subject:{self.config.gmail_filter_subject}")

        if self.config.gmail_filter_from:
            queries.append(f"from:{self.config.gmail_filter_from}")

        if self.config.gmail_filter_label:
            queries.append(f"label:{self.config.gmail_filter_label}")

        return " ".join(queries)

    def buscar_correos(
        self, max_results: int = 10, unread_only: bool = True
    ) -> List[EmailMessage]:
        """Busca correos según filtros configurados"""
        query = self._construir_query()

        if unread_only:
            query += " is:unread"

        print(f"🔍 Buscando correos: {query}")

        try:
            results = (
                self.service.users()
                .messages()
                .list(userId="me", q=query, maxResults=max_results)
                .execute()
            )

            messages = results.get("messages", [])

            email_messages = []
            for msg in messages:
                email_msg = self._procesar_mensaje(msg["id"])
                if email_msg:
                    email_messages.append(email_msg)

            return email_messages

        except HttpError as error:
            print(f"❌ Error buscando correos: {error}")
            return []

    def _procesar_mensaje(self, msg_id: str) -> Optional[EmailMessage]:
        """Procesa un mensaje y extrae información"""
        try:
            msg = (
                self.service.users()
                .messages()
                .get(userId="me", id=msg_id, format="full")
                .execute()
            )

            headers = msg["payload"]["headers"]

            subject = next(
                (h["value"] for h in headers if h["name"].lower() == "subject"), ""
            )
            sender = next(
                (h["value"] for h in headers if h["name"].lower() == "from"), ""
            )
            date_str = next(
                (h["value"] for h in headers if h["name"].lower() == "date"), ""
            )

            from email.utils import parsedate_to_datetime

            date = parsedate_to_datetime(date_str) if date_str else datetime.now()

            attachments = self._extraer_adjuntos(msg)

            return EmailMessage(
                id=msg["id"],
                thread_id=msg["threadId"],
                subject=subject,
                sender=sender,
                date=date,
                has_attachments=len(attachments) > 0,
                attachments=attachments,
            )

        except HttpError as error:
            print(f"❌ Error procesando mensaje: {error}")
            return None

    def _extraer_adjuntos(self, msg: Dict[str, Any]) -> List[EmailAttachment]:
        """Extrae archivos adjuntos de un mensaje"""
        attachments = []

        def procesar_parte(part: Dict[str, Any]):
            if "filename" in part and part["filename"]:
                if "body" in part and "attachmentId" in part["body"]:
                    try:
                        attachment_id = part["body"]["attachmentId"]
                        attachment = (
                            self.service.users()
                            .messages()
                            .attachments()
                            .get(userId="me", messageId=msg["id"], id=attachment_id)
                            .execute()
                        )

                        data = base64.urlsafe_b64decode(
                            attachment["data"].encode("UTF-8")
                        )

                        att = EmailAttachment(
                            filename=part["filename"],
                            mime_type=part["mimeType"],
                            data=data,
                            size=attachment["size"],
                        )
                        attachments.append(att)
                    except HttpError as error:
                        print(f"⚠️  Error extrayendo adjunto: {error}")

            if "parts" in part:
                for subpart in part["parts"]:
                    procesar_parte(subpart)

        if "parts" in msg["payload"]:
            for part in msg["payload"]["parts"]:
                procesar_parte(part)

        return attachments

    def marcar_como_leido(self, msg_id: str) -> None:
        """Marca un mensaje como leído"""
        try:
            self.service.users().messages().modify(
                userId="me", id=msg_id, body={"removeLabelIds": ["UNREAD"]}
            ).execute()
        except HttpError as error:
            print(f"⚠️  Error marcando como leído: {error}")

    def extraer_excel_adjuntos(self, correo: EmailMessage) -> List[EmailAttachment]:
        """
        Extrae solo los adjuntos Excel de un correo

        Args:
            correo: Mensaje de email

        Returns:
            Lista de adjuntos Excel
        """
        return [
            att
            for att in correo.attachments
            if att.filename.lower().endswith((".xlsx", ".xls"))
        ]
