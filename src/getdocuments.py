import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time
import hashlib

def generate_direct_download_url(wiki_urls): #usa hash para conseguir el link de descarga directa
    
    base_url = "https://delicias.dia.fi.upm.es/wiki/images/"
    download_urls = []

    for url in wiki_urls:
        
        file_name = url.split(":")[-1]  

        
        hash_md5 = hashlib.md5(file_name.encode()).hexdigest()

        
        dir1, dir2 = hash_md5[0], hash_md5[0:2]

        
        direct_url = f"{base_url}{dir1}/{dir2}/{file_name}"
        download_urls.append(direct_url)
    
    return download_urls



def load_urls_from_file(filepath):
    """Lee el archivo .txt con URLs y convierte las URLs en formato wiki a URLs directas de descarga."""
    with open(filepath, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]

    
    wiki_urls = [url for url in urls if "index.php/File:" in url]
    direct_urls = generate_direct_download_url(wiki_urls)

    
    final_urls = [
        direct_urls[wiki_urls.index(url)] if url in wiki_urls else url
        for url in urls
    ]
    
    return final_urls

def download_file(url, download_path):
    #time.sleep(1)
    """Descarga el archivo desde la URL y lo guarda en la ruta de destino."""
    local_filename = os.path.join(download_path, url.split("/")[-1])
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(local_filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    print(f"Archivo descargado: {local_filename}")


firefox_options = Options()
firefox_options.add_argument("--headless")


geckodriver_path = 'C:/Users/Jaime Vázquez/AppData/Local/Programs/Python/Python313/geckodriver.exe'
service = Service(geckodriver_path)
driver = webdriver.Firefox(service=service, options=firefox_options)


login_url = "https://delicias.dia.fi.upm.es/wiki/index.php?title=Special:UserLogin&returnto=Main+Page&returntoquery="
username = "jaime.vrivera"
password = "9rScwwFGLZDNfGz"


download_path = "./tfg/documentosnexo/"
os.makedirs(download_path, exist_ok=True)


driver.get(login_url)
time.sleep(2)

username_input = driver.find_element(By.ID, "wpName1")
password_input = driver.find_element(By.ID, "wpPassword1")
login_button = driver.find_element(By.ID, "wpLoginAttempt")

username_input.send_keys(username)
password_input.send_keys(password)
login_button.click()

time.sleep(3)

if "Especial:Entrar" not in driver.current_url:
    print("Inicio de sesión exitoso")
    
    
    urls_file = "./tfg/paginas3.txt"  # Cambiar esto
    urls = load_urls_from_file(urls_file)
    
    # Las url deberían acabar en eso pero por si acaso lo comprobamos
    for url in urls:
        if url.endswith((".ppt", ".pptx", ".pdf")):
            print(f"Descargando archivo desde: {url}")
            download_file(url, download_path)
        

else:
    print("Error en el inicio de sesión")

driver.quit()
