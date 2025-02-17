import os
import subprocess

class PPTtoPPTXConverter:
    def __init__(self, directory, libreoffice_path):
        """Inicializa el convertidor con el directorio de archivos PPT y abre la aplicación de PowerPoint."""
        self.directory = directory
        self.libreoffice_path = libreoffice_path

    def listar_ppt(self):
        """Lista todos los archivos PPT en el directorio especificado."""
        return [
            os.path.join(self.directory, archivo)
            for archivo in os.listdir(self.directory)
            if archivo.lower().endswith('.ppt')
        ]
    
    def convertir_ppt_a_pptx(self, input_file, output_dir):
        comando = [self.libreoffice_path, "--headless", "--convert-to", "pptx", "--outdir", output_dir, input_file]
        #print("Me meto")
        subprocess.run(comando, check=True)
        #print("Salgo")
    
    def convert_to_pttx(self):
        """Convierte cada archivo PPT en el directorio a PDF."""
        ppt_files = self.listar_ppt()
    
        #print(archivos_ppt_sin_pdf)
        
        for ppt_file in ppt_files:
            
            pptx_file = ppt_file.replace('.ppt', '.pttx')
            
            #print(pdf_file)
            
            if os.path.isfile(pptx_file):
                print(f"Se ha ignorado, ya se encuentra el fichero {pptx_file}")
                continue
            
            try:
                print(f"Convirtiendo {ppt_file} a {pptx_file}...")
                
                # Ejemplo de uso
                self.convertir_ppt_a_pptx(ppt_file, self.directory)
                
                
                print(f"Conversión completada: {pptx_file}")
            except Exception as e:
                print(f"Error al convertir {ppt_file} a PDF: {e}")


