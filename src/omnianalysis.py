from analisisppt import PPTXProcessor
from pdfanalysis import PDFProcessor
from ppttopdf import PPTtoPDFConverter
from analisiswiki import WikiAnalysis
from scapingpaginas import WikiAllPageScraper
from getdocuments import WikiDownloader
#Dando los datos de usuario y las rutas descarga todo
#Para cambiar la base de datos, ver el fichero de pineconeupload
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()
    
username = open_file('C:/Users/Jaime Vázquez/Documents/Python/username_oeg.txt')

password = open_file('C:/Users/Jaime Vázquez/Documents/Python/password_oeg.txt')

geckodriver_path = 'C:/Users/Jaime Vázquez/AppData/Local/Programs/Python/Python313/geckodriver.exe'
wiki_urls = [
        "https://delicias.dia.fi.upm.es/wiki/index.php/Special:AllPages",
        "https://delicias.dia.fi.upm.es/wiki/index.php?title=Special:AllPages&from=Licencias"
    ]

paginas_path = "C:/Users/Jaime Vázquez/Documents/Python/tfg/textos/paginas.txt"
presentaciones_link_path = "C:/Users/Jaime Vázquez/Documents/Python/tfg/textos/enlaces_presentaciones.txt"
documents_path = "C:/Users/Jaime Vázquez/Documents/Python/tfg/documentosnexo/"



mi_scraper_all = WikiAllPageScraper(username, password, geckodriver_path, paginas_path)

miWikiAnalysis= WikiAnalysis(username, password, geckodriver_path, paginas_path, presentaciones_link_path)

miWikiDownloader = WikiDownloader(username, password, geckodriver_path, documents_path)

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


        
miPDFconverter = PPTtoPDFConverter(documents_path)
miPPTXProcessor= PPTXProcessor(documents_path)
miPDFProcessor= PDFProcessor(documents_path)

miPDFconverter.convert_to_pdf()
miPDFconverter.close()

miPPTXProcessor.analyze_and_upload()
miPDFProcessor.analyze_and_upload()

print("\n\nFIN\n\n")