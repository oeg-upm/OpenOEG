from src.analisisppt import PPTXProcessor
from src.pdfanalysis import PDFProcessor
#from ppttopdf import PPTtoPDFConverter
from src.analisiswiki import WikiAnalysis
from src.scapingpaginas import WikiAllPageScraper
from src.getdocuments import WikiDownloader
from src.ppttopttx import PPTtoPPTXConverter
import yaml
#Dando los datos de usuario y las rutas descarga todo
#Para cambiar la base de datos, ver el fichero de pineconeupload
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()
    
#username = open_file('./textos/username_oeg.txt')

#password = open_file('./textos/password_oeg.txt')


with open('config2.yaml', 'r') as yaml_file:
    config = yaml.safe_load(yaml_file)


username = config["config"]["credentials"]["oeg"]["username"]
password = config["config"]["credentials"]["oeg"]["password"]
libreoffice_path = config["config"]["paths"]["libreoffice"]

paginas_path = "./textos/paginas.txt"
presentaciones_link_path = "./textos/enlaces_presentaciones.txt"
documents_path = "./documentosnexo/"

driver_path = config["config"]["paths"]["driver"]
wiki_urls = [
        "https://delicias.dia.fi.upm.es/wiki/index.php/Special:AllPages",
        "https://delicias.dia.fi.upm.es/wiki/index.php?title=Special:AllPages&from=Licencias"
    ]



mi_scraper_all = WikiAllPageScraper(username, password, driver_path, paginas_path)

miWikiAnalysis= WikiAnalysis(username, password, driver_path, paginas_path, presentaciones_link_path)

miWikiDownloader = WikiDownloader(username, password, driver_path, documents_path)

if not mi_scraper_all.login():
    print("Error en el inicio de sesión")
else:
    print("Inicio de sesión exitoso")
   
    mi_scraper_all.scrape_and_save_urls(wiki_urls)
    
mi_scraper_all.close()
    
if not miWikiAnalysis.login():
    print("Error en el inicio de sesión")
else:
    miWikiAnalysis.scrape_pages()
        
miWikiAnalysis.close()
        
if not miWikiDownloader.login():
    print("Error en el inicio de sesión")      
else:
    
    urls = miWikiDownloader.load_urls_from_file(presentaciones_link_path)
    miWikiDownloader.download_files_from_urls(urls)
    
miWikiDownloader.close()


        
#miPDFconverter = PPTtoPDFConverter(documents_path)
miPPTXConverter= PPTtoPPTXConverter(documents_path, libreoffice_path)
miPPTXProcessor= PPTXProcessor(documents_path)
miPDFProcessor= PDFProcessor(documents_path)


#miPDFconverter.convert_to_pdf()
#miPDFconverter.close()
miPPTXConverter.convert_to_pttx()

miPPTXProcessor.analyze_and_upload()
miPDFProcessor.analyze_and_upload()

print("\n\nFIN\n\n")