from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from src.pineconeupload import PineconeUploader
import time
import csv
from langchain.text_splitter import RecursiveCharacterTextSplitter
#from langchain_community.vectorstores.utils import filter_complex_metadata

def open_file(filepath):
        """Lee las páginas desde el archivo dado."""
        with open(filepath, 'r', encoding='utf-8') as infile:
            return [pagina for pagina in infile.read().splitlines() if pagina.strip()]


class WikiAnalysis:
    def __init__(self, username, password, geckodriver_path, paginas_file='./textos/paginas.txt', presentaciones_file = "./textos/enlaces_presentaciones.txt"):
        # Configuración de opciones de Firefox
        firefox_options = Options()
        firefox_options.add_argument("--headless")

        self.username = username
        self.password = password
        self.driver = webdriver.Firefox(service=Service(geckodriver_path), options=firefox_options)
        self.paginas_file = paginas_file
        self.pcuploader = PineconeUploader()
        self.presentaciones_file = presentaciones_file
    

    def login(self):
        """Realiza el inicio de sesión en el sitio wiki."""
        login_url = "https://delicias.dia.fi.upm.es/wiki/index.php?title=Special:UserLogin&returnto=Main+Page&returntoquery="
        self.driver.get(login_url)
        time.sleep(2)

        username_input = self.driver.find_element(By.ID, "wpName1")
        password_input = self.driver.find_element(By.ID, "wpPassword1")
        login_button = self.driver.find_element(By.ID, "wpLoginAttempt")

        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        login_button.click()
        time.sleep(3)

        return "Especial:Entrar" not in self.driver.current_url

    def save_links_to_file(self, links, filename):
        """Guarda solo el primer enlace de presentación en un archivo de texto."""
        with open(filename, 'a', encoding='utf-8') as file:
            for link in links:
                file.write(link + '\n')

    def divide_text(self, text):
        #texts = [] https://delicias.dia.fi.upm.es/wiki/index.php/Charlas
        
        texts = RecursiveCharacterTextSplitter(chunk_size=8180, chunk_overlap=100).split_text(text) #https://medium.com/@vndee.huynh/build-your-own-rag-and-run-it-locally-langchain-ollama-streamlit-181d42805895
        # sacado de https://huggingface.co/jinaai/jina-embeddings-v2-base-es 
        # un poco menos para que entre lo la parte de get_embedding
        #texts = filter_complex_metadata(texts)
        
        return texts

    #def scrape_pages_charlas(self):
    #    pagina = "https://delicias.dia.fi.upm.es/wiki/index.php/Charlas"
    #    
    #    self.driver.get(pagina)
    #    time.sleep(2)   
    #    soup = BeautifulSoup(self.driver.page_source, 'html.parser')
    #    tables = soup.find_all('table') 
    #
    #    
    #    for table in tables:
    #        rows = table.find_all('tr')
    #        for row in rows:
    #            cols = row.find_all(['td', 'th'])
    #            full_text = []
    #            links_found = []
    #            for col in cols:
    #                text = col.get_text(separator=" ", strip=True)
    #                link_tag = col.find('a')
    #                if link_tag and link_tag.has_attr('href'):
    #                    href = link_tag['href']
    #                    if href.startswith('/'):
    #                        href = "https://delicias.dia.fi.upm.es" + href
    #                    links_found.append(href)
    #                    
    #                if href.startswith("https://delicias.dia.fi.upm.es/wiki/index.php/"):
    #                    full_text.append(text)
    #            if links_found:
    #                # Guarda una línea por cada enlace encontrado, junto al resto del texto
    #                for link in links_found:
    #                    writer.writerow(['\t'.join(full_text), link])
                        

    def scrape_pages_charlas(self):
        from bs4 import BeautifulSoup
        import time

        pagina = "https://delicias.dia.fi.upm.es/wiki/index.php/Charlas"
        
        self.driver.get(pagina)
        time.sleep(2)   
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        tables = soup.find_all('table') 
        etiquetas = ["Date", "Place", "Speaker", "Topic"]
        links_totales = []
        mi_dict = {}

        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all(['td', 'th'])
                texto_total = []
                for col in cols:
                    text = col.get_text(separator=" ", strip=True)
                    link_tag = col.find('a')
                    
                    
                    for i, etiqueta in enumerate(etiquetas):
                        if len(texto_total) == i:
                            texto_total.append(f"{etiqueta}: {text}")
                            break  
                        
                    if link_tag and link_tag.has_attr('href'):
                        href = link_tag['href']
                        
                        # Corrige si es http
                        href = href.replace("http:", "https:")
                        
                        if href.startswith('/'):
                            href = "https://delicias.dia.fi.upm.es" + href
                        
                        # Asegúrate de que sea un fichero válido
                        if href.startswith("https://delicias.dia.fi.upm.es/wiki/") and href.endswith(('.ppt', '.pptx', '.pdf')):
                            #print(href)
                            nombre_fichero = href.split('/')[-1]
                            if nombre_fichero.endswith('.ppt'):
                                nombre_fichero = nombre_fichero.replace('.ppt', '.pptx')
                            mi_dict[nombre_fichero] = texto_total
                            links_totales.append(href)

        return [links_totales, mi_dict]


    
    def scrape_pages(self):
        """Recorre cada página, busca y guarda enlaces a presentaciones."""
        paginas = open_file(self.paginas_file)
        open(self.presentaciones_file, 'w').close()  # Limpia el archivo de enlaces previo

        diccionario_charlas = {}
        
        for pagina in paginas:
            
            if pagina == "https://delicias.dia.fi.upm.es/wiki/index.php/Charlas":
                
                par = self.scrape_pages_charlas()
                diccionario_charlas = par[1]
                self.save_links_to_file(par[0], self.presentaciones_file)
                continue
            
            self.driver.get(pagina)
            time.sleep(2)

            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            content_div = soup.select_one('div.mw-content-ltr')

            # Extraer texto útil (opcionalmente puede usarse PineconeUploader aquí)
            if content_div:
                useful_text = content_div.get_text(separator="\n", strip=True).replace("[\nedit\n]", "")
                
                #TODO pagina de charlas especial https://delicias.dia.fi.upm.es/wiki/index.php/Charlas
                
                divided_texts = self.divide_text(useful_text)
                
                for text in divided_texts:
                    self.pcuploader.upload_text("Wiki: "+pagina  + " \n\n"+text, rol="SYSTEM") 

            # Extraer enlaces de presentaciones
            presentation_links = [
                link['href'].replace("http:", "https:") if link['href'].startswith("http:") 
                else link['href']
                for link in soup.find_all('a', href=True)
                if link['href'].endswith(('.ppt', '.pptx', '.pdf'))
            ]

            
            # Guardar enlaces encontrados, cambiar aquí TODO
            new_links = []
            
            
            
            if presentation_links:
                for link in presentation_links:
                    
                    if link.startswith("https://delicias.dia.fi.upm.es/wiki/index.php/"):
                        self.driver.get(link)
                        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                        

                        # Iterar sobre todos los enlaces que tengan un atributo 'href', hipervinculos
                        for link in soup.find_all('a', href=True):
                            href = link['href']
                            
                            # Verificar si el enlace termina en .ppt, .pptx o .pdf
                            if href.endswith(('.ppt', '.pptx', '.pdf')):
                                
                                # Realizar las transformaciones necesarias
                                transformed_link = "https://delicias.dia.fi.upm.es"+href
                                
                                if "title=Special" not in transformed_link: 
                                    new_links.append(transformed_link)
                                break
                    elif link.startswith("/wiki/"):
                        if "title=Special" not in link: #paginas erroneas
                            
                            new_links.append("https://delicias.dia.fi.upm.es" +link)
                    

                    else:
                        if "title=Special" not in link: #paginas erroneas
                            
                            new_links.append(link)
                                      
                        
            if new_links:
                #self.save_links_to_file(new_links, self.presentaciones_file)
                print(f"Enlaces guardados de {pagina}")
            else:
                print(f"No se encontraron enlaces a presentaciones en {pagina}")

        
        return diccionario_charlas
    def close(self):
        """Cierra el navegador."""
        self.driver.quit()
