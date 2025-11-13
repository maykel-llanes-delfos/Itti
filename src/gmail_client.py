import base64
import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from email import message_from_bytes


class GmailClient:
    def __init__(self, service_account_file: str, user_email: str):
        scopes = ["https://www.googleapis.com/auth/gmail.readonly"]
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file, scopes=scopes, subject=user_email
        )
        self.service = build("gmail", "v1", credentials=credentials)

    def search_messages(self, query: str):
        results = self.service.users().messages().list(userId="me", q=query).execute()
        return results.get("messages", [])

    def get_attachments(self, msg_id: str, output_dir: str):
        msg = self.service.users().messages().get(userId="me", id=msg_id).execute()
        payload = msg.get("payload", {})

        if "parts" not in payload:
            return []

        attachments = []
        for part in payload["parts"]:
            if part.get("filename") and "attachmentId" in part.get("body", {}):
                att_id = part["body"]["attachmentId"]
                data = (
                    self.service.users()
                    .messages()
                    .attachments()
                    .get(userId="me", messageId=msg_id, id=att_id)
                    .execute()
                )

                file_data = base64.urlsafe_b64decode(data["data"].encode("UTF-8"))
                file_path = os.path.join(output_dir, part["filename"])

                with open(file_path, "wb") as f:
                    f.write(file_data)
                attachments.append(file_path)

                return attachments
