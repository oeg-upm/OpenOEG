from pineconeupload import PineconeUploader
from pptx import Presentation
import os

class PPTXProcessor:
    def __init__(self, pptx_dir):
        """Inicializa la clase con el directorio donde se encuentran los archivos .pptx."""
        self.pptx_dir = pptx_dir
        self.pcuploader = PineconeUploader()

    def list_pptx(self):
        """Lista todos los archivos .pptx en el directorio especificado."""
        archivos_pptx = [archivo for archivo in os.listdir(self.pptx_dir) if archivo.lower().endswith('.pptx')]
        return archivos_pptx

    def extract_text(self, fichero):
        """Extrae texto de las diapositivas de un archivo .pptx y organiza el contenido."""
        presentation = Presentation(os.path.join(self.pptx_dir, fichero))
        textos = []

        for slide_number, slide in enumerate(presentation.slides, start=1):
            for shape in slide.shapes:
                if shape.has_text_frame:
                    text = shape.text_frame.text
                    if len(text) > 2:  # Filtro para omitir textos breves o vacíos
                        texto_formateado = f"{fichero}: Diapositiva {{{slide_number}}}\n{text}"
                        textos.append(texto_formateado)
        return textos

    def analyze_and_upload(self, rol="SYSTEM"):
        """Procesa todos los archivos .pptx en el directorio y sube el contenido extraído a Pinecone."""
        ficheros = self.list_pptx()

        for fichero in ficheros:
            textos = self.extract_text(fichero)
            if textos:  # Solo subir si hay textos válidos
                self.pcuploader.bulk_upload(textos, rol=rol)
                print(f"Contenido de {fichero} subido correctamente.")
            else:
                print(f"No se encontró contenido válido en {fichero}.")

# Ejemplo de uso
#pptx_path = "C:/Users/Jaime Vázquez/Documents/Python/tfg/ptts2/"  # Cambia esto por la ruta de tu directorio de archivos .pptx
#procesador = PPTXProcessor(pptx_path)
#procesador.procesar_y_subir(rol="SYSTEM")
