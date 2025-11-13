from googleapiclient.discovery import build
from google.oauth2 import service_account

# Archivo JSON descargado de la cuenta de servicio
SERVICE_ACCOUNT_FILE = "light-height-drive-235716-82ec9163785a.json"

# Scopes necesarios
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/drive.file",
]

# Si es dominio corporativo:
# credentials = service_account.Credentials.from_service_account_file(
#     SERVICE_ACCOUNT_FILE, scopes=SCOPES, subject='usuario@tu-dominio.com'
# )

# Si es cuenta personal con acceso a Gmail API:
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

gmail_service = build("gmail", "v1", credentials=credentials)
drive_service = build("drive", "v3", credentials=credentials)


def search_messages(query: str):
    results = gmail_service.users().messages().list(userId="me", q=query).execute()
    return results.get("messages", [])


def create_folder(name: str):
    file_metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    folder = drive_service.files().create(body=file_metadata, fields="id").execute()
    print(folder.get("id"))
    print(folder)
    return folder.get("id")


create_folder("Maykel Llanes")
