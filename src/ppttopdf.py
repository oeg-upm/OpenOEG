import comtypes.client
import os

class PPTtoPDFConverter:
    def __init__(self, directory):
        """Inicializa el convertidor con el directorio de archivos PPT y abre la aplicación de PowerPoint."""
        self.directory = directory
        self.powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
        self.powerpoint.Visible = 1

    def listar_ppt(self):
        """Lista todos los archivos PPT en el directorio especificado."""
        return [
            os.path.join(self.directory, archivo)
            for archivo in os.listdir(self.directory)
            if archivo.lower().endswith('.ppt')
        ]
    
    def convert_to_pdf(self):
        """Convierte cada archivo PPT en el directorio a PDF."""
        ppt_files = self.listar_ppt()
        

        
        #print(archivos_ppt_sin_pdf)
        
        for ppt_file in ppt_files:
            
            pdf_file = ppt_file.replace('.ppt', '.pdf')
            
            #print(pdf_file)
            
            if os.path.isfile(pdf_file):
                print(f"Se ha ignorado, ya se encuentra el fichero {pdf_file}")
                continue
            
            try:
                print(f"Convirtiendo {ppt_file} a {pdf_file}...")
                deck = self.powerpoint.Presentations.Open(os.path.abspath(ppt_file))
                deck.SaveAs(os.path.abspath(pdf_file), 32)  # 32 es el formato para guardar como PDF
                deck.Close()
                print(f"Conversión completada: {pdf_file}")
            except Exception as e:
                print(f"Error al convertir {ppt_file} a PDF: {e}")

    def close(self):
        """Cierra la aplicación de PowerPoint."""
        self.powerpoint.Quit()

""" # Ejemplo de uso
file_path = r"C:/Users/Jaime Vázquez/Documents/Python/tfg/ptts2/"
converter = PPTtoPDFConverter(file_path)
converter.convert_to_pdf()
converter.close()
 """