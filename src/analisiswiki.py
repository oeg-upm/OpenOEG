from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
from pineconeupload import PineconeUploader

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()



paginas = open_file('./tfg/paginas2.txt').split("\n")
paginas = [pagina for pagina in paginas if pagina.strip()]

firefox_options = Options()
firefox_options.add_argument("--headless")

geckodriver_path = 'C:/Users/Jaime Vázquez/AppData/Local/Programs/Python/Python313/geckodriver.exe'
service = Service(geckodriver_path)
driver = webdriver.Firefox(service=service, options=firefox_options)

# URL de inicio de sesión
login_url = "https://delicias.dia.fi.upm.es/wiki/index.php?title=Special:UserLogin&returnto=Main+Page&returntoquery="
driver.get(login_url)
time.sleep(2)

username_input = driver.find_element(By.ID, "wpName1")
password_input = driver.find_element(By.ID, "wpPassword1")
login_button = driver.find_element(By.ID, "wpLoginAttempt")

username = "jaime.vrivera"
password = "9rScwwFGLZDNfGz"
username_input.send_keys(username)
password_input.send_keys(password)
login_button.click()
time.sleep(3)

# Verificar autenticación
if "Especial:Entrar" not in driver.current_url:
    print("Inicio de sesión exitoso")

    #pcuploader = PineconeUploader()
    
    for pagina in paginas:
        payload = list()
        driver.get(pagina)
        time.sleep(2)

        page_content = driver.page_source
        soup = BeautifulSoup(page_content, 'html.parser')
        content_div = soup.select_one('div.mw-content-ltr')
        
        if content_div:
            useful_text = content_div.get_text(separator="\n", strip=True).replace("[\nedit\n]", "")
            
            #pcuploader.upload_text(useful_text, role = "SYSTEM")
        else:
            print("No se encontró el contenido principal en esta página.") 
        

        presentation_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.endswith(( '.ppt')): #', '.pptx', '.pdf'
                presentation_links.append(href.replace("http","https" ))

        if presentation_links:
            print("\nEnlaces a presentaciones encontradas:") #TODO referenciar de alguna manera el origen?
            for presentation in presentation_links:
                print(presentation)
        else:
            print("\nNo se encontraron enlaces a presentaciones en esta página.")

    
    driver.quit()

else:
    print("Error en el inicio de sesión")
    driver.quit()





