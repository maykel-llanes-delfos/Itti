from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field, EmailStr, field_validator


class Cliente(BaseModel):
    """Modelo de datos para un cliente"""

    nombre: str = Field(..., min_length=1)
    apellido1: str = Field(..., min_length=1)
    apellido2: str = Field(..., min_length=1)

    @field_validator("nombre", "apellido1", "apellido2")
    @classmethod
    def validar_mayusculas(cls, v: str) -> str:
        return v.strip().upper()

    @property
    def nombre_carpeta(self) -> str:
        return f"{self.nombre} {self.apellido1} {self.apellido2}"


class ArchivoCliente(BaseModel):
    """Modelo para archivos a subir"""

    ruta_local: Optional[str] = Field(None, description="Ruta local del archivo")
    contenido_bytes: Optional[bytes] = Field(None, description="Contenido en bytes")
    nombre_destino: str = Field(..., description="Nombre del archivo en Drive")
    mime_type: str = Field(default="application/octet-stream")

    @field_validator("ruta_local")
    @classmethod
    def validar_archivo_existe(cls, v: Optional[str]) -> Optional[str]:
        if v and not Path(v).exists():
            raise ValueError(f"El archivo no existe: {v}")
        return v

    def validar_contenido(self):
        """Valida que exista ruta_local o contenido_bytes"""
        if not self.ruta_local and not self.contenido_bytes:
            raise ValueError("Debe proporcionar ruta_local o contenido_bytes")


class EmailAttachment(BaseModel):
    """Modelo para archivos adjuntos de email"""

    filename: str
    mime_type: str
    data: bytes
    size: int = Field(gt=0)


class EmailMessage(BaseModel):
    """Modelo para mensajes de email"""

    id: str
    thread_id: str
    subject: str
    sender: str
    date: datetime
    has_attachments: bool = False
    attachments: List[EmailAttachment] = Field(default_factory=list)


class DriveFileChange(BaseModel):
    """Modelo para cambios en archivos de Drive"""

    file_id: str
    file_name: str
    modified_time: datetime
    mime_type: str
    parent_folder: str
    web_view_link: Optional[str] = None


class ExcelData(BaseModel):
    """Modelo para datos leídos de Excel"""

    file_id: str
    file_name: str
    sheet_names: List[str]
    data: Dict[str, List[Dict[str, Any]]]  # {sheet_name: [rows]}
    modified_time: datetime
