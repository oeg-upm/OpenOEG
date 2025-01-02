import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options


class WikiDownloader: #TODO archivos repetidos?
    def __init__(self, username, password, geckodriver_path, download_path="./tfg/documentosnexo/"):
        self.username = username
        self.password = password
        self.download_path = download_path

        # Configuración del navegador Firefox en modo headless
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        self.driver = webdriver.Firefox(service=Service(geckodriver_path), options=firefox_options)

        # Crear el directorio de descarga si no existe
        os.makedirs(self.download_path, exist_ok=True)

    def login(self):
        """Realiza el inicio de sesión en el sitio wiki."""
        login_url = "https://delicias.dia.fi.upm.es/wiki/index.php?title=Special:UserLogin&returnto=Main+Page&returntoquery="
        self.driver.get(login_url)
        time.sleep(2)

        # Completa los campos de inicio de sesión y envía el formulario
        self.driver.find_element(By.ID, "wpName1").send_keys(self.username)
        self.driver.find_element(By.ID, "wpPassword1").send_keys(self.password)
        self.driver.find_element(By.ID, "wpLoginAttempt").click()
        time.sleep(3)

        # Verifica si la autenticación fue exitosa
        return "Especial:Entrar" not in self.driver.current_url


    def load_urls_from_file(self, filepath):
        """Carga las URLs desde un archivo y convierte las URLs wiki a URLs de descarga directa."""
        with open(filepath, 'r') as file:
            urls = [line.strip() for line in file if line.strip()]

        wiki_urls = [url for url in urls if "index.php/" in url]
        

        final_urls = [
            wiki_urls[wiki_urls.index(url)] if url in wiki_urls else url
            for url in urls
        ]
        
        return final_urls

    def download_file(self, url):
        """Descarga el archivo desde la URL y lo guarda en la ruta de destino."""
        local_filename = os.path.join(self.download_path, url.split("/")[-1])
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(local_filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        print(f"Archivo descargado: {local_filename}")

    def download_files_from_urls(self, urls):
        """Descarga archivos desde una lista de URLs."""
        #print(urls)
        
        for url in urls:
            #print(os.path.join(self.download_path, url.split("/")[-1]))
            if url.endswith((".ppt", ".pptx", ".pdf")) and url.startswith("https://delicias.dia.fi.upm.es/wiki/") and not os.path.isfile( os.path.join(self.download_path, url.split("/")[-1])): #filtrar resultados que no sean de la página y los que ya estan
                print(f"Descargando archivo desde: {url}")
                self.download_file(url)

    def close(self):
        """Cierra el navegador."""
        self.driver.quit()


""" # Uso de la clase
username = "jaime.vrivera"
password = "9rScwwFGLZDNfGz"
geckodriver_path = 'C:/Users/Jaime Vázquez/AppData/Local/Programs/Python/Python313/geckodriver.exe'

downloader = WikiDownloader(username, password, geckodriver_path)

if downloader.login():
    print("Inicio de sesión exitoso")

    # Cargar URLs desde el archivo
    urls_file = "./tfg/paginas3.txt"
    urls = downloader.load_urls_from_file(urls_file)

    # Descargar archivos
    downloader.download_files_from_urls(urls)
else:
    print("Error en el inicio de sesión")

# Cerrar el navegador
downloader.close() """
