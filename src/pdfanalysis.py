import os
import pymupdf 
from src.pineconeupload import PineconeUploader
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter

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

    def divide_text(self, text):
        #texts = []
        
        texts = RecursiveCharacterTextSplitter(chunk_size=8180, chunk_overlap=100).split_text(text) #https://medium.com/@vndee.huynh/build-your-own-rag-and-run-it-locally-langchain-ollama-streamlit-181d42805895
        # sacado de https://huggingface.co/jinaai/jina-embeddings-v2-base-es 
        # un poco menos para que entre lo la parte de get_embedding
        #texts = filter_complex_metadata(texts)
        
        return texts
    
    def extract_text(self, document, file_name):
        """Extrae el texto de cada página del PDF y lo guarda en una lista."""
        text_by_page = []
        for page_num in range(document.page_count):
            page = document[page_num]
            text = page.get_text("text")
            
            if text.strip():  # Filtrar páginas sin texto
            
                divided_texts = self.divide_text(text)
                    
                for text in divided_texts:
                            
                    texto_formateado = f"{file_name}: Página {{{page_num+1}}}\n{text}"
                    text_by_page.append(texto_formateado)
            
            
        return text_by_page

    def analyze_and_upload(self):
        """Analiza y sube el contenido de cada PDF en el directorio a Pinecone."""
        ficheros = self.listar_pdf()

        for fichero in ficheros:
            
            if os.path.getsize(fichero) < 8192:  # 8 KB = 8192 bytes, es un archivo roto seguramente
                print(f"Archivo omitido por ser roto: {os.path.basename(fichero)}")
                continue
            
            
            #res = ""
            
            try:
                document = pymupdf.open(fichero)
            except Exception as e:
                print(f"Error al abrir el archivo: {e}")
                continue
                
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
            
