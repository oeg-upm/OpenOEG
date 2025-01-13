import os
import pymupdf 
from pineconeupload import PineconeUploader
import json

def json_to_str(json_obj):
    try:
        json_str = json.dumps(json_obj, indent=4, ensure_ascii=False)
        return json_str
    except (TypeError, ValueError) as e:
        print(f"Error al convertir JSON a cadena: {e}")
        return None



class PDFProcessor:
    def __init__(self, directory_path):
        """Inicializa la clase con el directorio que contiene archivos PDF y el uploader de Pinecone."""
        self.directory_path = directory_path
        self.pcuploader = PineconeUploader()

    def listar_pdf(self):
        """Lista todos los archivos PDF en el directorio especificado."""
        return [
            os.path.join(self.directory_path, archivo)
            for archivo in os.listdir(self.directory_path)
            if archivo.lower().endswith('.pdf')
        ]

    def get_metadata(self, document):
        """Obtiene los metadatos del documento PDF."""
        return json_to_str(document.metadata)

    def extract_text(self, document, file_name):
        """Extrae el texto de cada página del PDF y lo guarda en una lista."""
        text_by_page = []
        for page_num in range(document.page_count):
            page = document[page_num]
            text = page.get_text("text")
            if text.strip():  # Filtrar páginas sin texto
                formatted_text = f"{file_name}: Página {page_num + 1}\n{text}"
                text_by_page.append(formatted_text)
        return text_by_page

    def analyze_and_upload(self):
        """Analiza y sube el contenido de cada PDF en el directorio a Pinecone."""
        ficheros = self.listar_pdf()

        for fichero in ficheros:
            
            if os.path.getsize(fichero) < 8192:  # 8 KB = 8192 bytes, es un archivo roto seguramente
                print(f"Archivo omitido por ser roto: {os.path.basename(fichero)}")
                continue
            
            
            #res = ""
            document = pymupdf.open(fichero)
            metadata = os.path.basename(fichero) + " metadatos " + self.get_metadata(document)
            text_content = self.extract_text(document, os.path.basename(fichero))
            
            if not text_content:
                print(f"Archivo omitido por no tener texto: {os.path.basename(fichero)}")
                document.close()
                continue
            #MuPDF error: format error: No default Layer config
            #error a ignorar
            """ 
            for texto in text_content:
                res=res + " " + texto  """
            
            # Subir los metadatos y el contenido de texto a Pinecone
            
            
            self.pcuploader.upload_text(metadata, "SYSTEM")
            #self.pcuploader.upload_text(res, "SYSTEM")
            self.pcuploader.bulk_upload(text_content, "SYSTEM")
           
            
            document.close()
            print(f"Procesado y subido: {os.path.basename(fichero)}")
            




"""  # Ejemplo de uso
file_path = "C:/Users/Jaime Vázquez/Documents/Python/tfg/documentosnexo/"  # Cambiar esta ruta
pdf_processor = PDFProcessor(file_path)
#print(pdf_processor.get_metadata(file_path+"AMPER08_-_Introduction_to_SPARQL.pdf"))
pdf_processor.analyze_and_upload() 
 """