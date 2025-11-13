"""Generador de archivos placeholder para testing"""

import io
import pandas as pd

from models.schemas import ArchivoCliente


class PlaceholderGenerator:
    """Generador de archivos placeholder para testing"""

    @staticmethod
    def crear_imagen_placeholder(
        nombre: str, ancho: int = 800, alto: int = 600, color: str = "blue"
    ) -> ArchivoCliente:
        """
        Crea una imagen placeholder en memoria

        Args:
            nombre: Nombre del archivo
            ancho: Ancho de la imagen
            alto: Alto de la imagen
            color: Color de la imagen

        Returns:
            ArchivoCliente con la imagen en memoria
        """
        try:
            from PIL import Image, ImageDraw

            # Crear imagen
            img = Image.new("RGB", (ancho, alto), color=color)
            draw = ImageDraw.Draw(img)

            # Agregar texto
            text = f"PLACEHOLDER\n{nombre}"
            bbox = draw.textbbox((0, 0), text)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            position = ((ancho - text_width) // 2, (alto - text_height) // 2)
            draw.text(position, text, fill="white")

            # Convertir a bytes
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="PNG")
            img_bytes.seek(0)

            return ArchivoCliente(
                contenido_bytes=img_bytes.read(),
                nombre_destino=nombre,
                mime_type="image/png",
            )

        except ImportError:
            # Si PIL no está disponible, crear archivo de texto
            print("⚠️  PIL no disponible, creando placeholder de texto")
            contenido = f"PLACEHOLDER IMAGE: {nombre}".encode("utf-8")

            return ArchivoCliente(
                contenido_bytes=contenido, nombre_destino=nombre, mime_type="text/plain"
            )

    @staticmethod
    def crear_excel_placeholder(nombre: str = "placeholder.xlsx") -> ArchivoCliente:
        """
        Crea un archivo Excel placeholder

        Args:
            nombre: Nombre del archivo

        Returns:
            ArchivoCliente con el Excel en memoria
        """
        # Crear DataFrame de ejemplo
        df = pd.DataFrame(
            {
                "ID": range(1, 11),
                "Nombre": [f"Item {i}" for i in range(1, 11)],
                "Cantidad": [i * 10 for i in range(1, 11)],
                "Precio": [i * 100.5 for i in range(1, 11)],
            }
        )

        # Guardar en memoria
        excel_bytes = io.BytesIO()
        df.to_excel(excel_bytes, index=False, sheet_name="Datos")
        excel_bytes.seek(0)

        return ArchivoCliente(
            contenido_bytes=excel_bytes.read(),
            nombre_destino=nombre,
            mime_type="application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet",
        )
