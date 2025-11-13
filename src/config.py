import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv


load_dotenv()


class GmailSettings(BaseModel):
    user: str = Field(..., alias="GMAIL_USER")
    filter_from: str | None = Field(None, alias="GMAIL_FILTER_FROM")
    filter_subject: str | None = Field(None, alias="GMAIL_FILTER_SUBJECT")
    filter_label: str | None = Field(None, alias="GMAIL_FILTER_LABEL")


class DriveSettings(BaseModel):
    root_folder_id: str = Field(..., alias="DRIVE_ROOT_FOLDER_ID")
    folder_template: str = Field(..., alias="DRIVE_CLIENT_FOLDER_TEMPLATE")


class JobSettings(BaseModel):
    tmp_dir: str = Field(..., alias="DOWNLOAD_TMP_DIR")
    poll_interval: int = Field(..., alias="POLL_INTERVAL_SECONDS")
    log_level: str = Field(..., alias="LOG_LEVEL")


class GoogleAuthSettings(BaseModel):
    service_account_file: str = Field(..., alias="GOOGLE_SERVICE_ACCOUNT_FILE")


class Settings(BaseModel):
    gmail: GmailSettings
    drive: DriveSettings
    job: JobSettings
    google_auth: GoogleAuthSettings


def load_settings() -> Settings:
    return Settings(
        gmail=GmailSettings(**os.environ),
        drive=DriveSettings(**os.environ),
        job=JobSettings(**os.environ),
        google_auth=GoogleAuthSettings(**os.environ),
    )
