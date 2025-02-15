# ahí están los ppw (muchos)
# https://delicias.dia.fi.upm.es/wiki/index.php/Transparencias

# Todas las páginas
#
# https://delicias.dia.fi.upm.es/wiki/index.php/Special:AllPages


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time


#Saca todas las páginas de una wiki utilizando la página especial de AllPages

class WikiAllPageScraper:
    def __init__(self, username, password, geckodriver_path, output_file="./tfg/textos/paginas.txt"):

        self.output_file = output_file
        self.username = username
        self.password = password

        firefox_options = Options()
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Firefox(service=Service(geckodriver_path), options=firefox_options)

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

        
        return "Especial:Entrar" not in self.driver.current_url

    def scrape_and_save_urls(self, urls_to_scrape):
        """Navega por cada URL de página wiki y guarda los enlaces en un archivo."""
        # Limpia el archivo de salida antes de escribir nuevos enlaces
        open(self.output_file, 'w').close()

        # Itera sobre cada página de la lista
        for wiki_url in urls_to_scrape:
            self.driver.get(wiki_url)
            time.sleep(2)

            # Obtiene todos los enlaces en la página
            page_links = self.driver.find_elements(By.CSS_SELECTOR, 'ul.mw-allpages-chunk li a')
            urls = [link.get_attribute('href') for link in page_links]

            # Guarda los enlaces encontrados en el archivo
            if urls:
                with open(self.output_file, 'a', encoding='utf-8') as file:
                    for url in urls:
                        file.write(url + '\n')
                print(f"URLs guardadas de {wiki_url}")

    def close(self):
        """Cierra el navegador."""
        self.driver.quit()

# Uso de la clase
""" username = "jaime.vrivera"
password = "9rScwwFGLZDNfGz"
geckodriver_path = 'C:/Users/Jaime Vázquez/AppData/Local/Programs/Python/Python313/geckodriver.exe'

scraper = WikiPageScraper(username, password, geckodriver_path)
if scraper.login():
    print("Inicio de sesión exitoso")

    # Páginas wiki para recorrer
    wiki_urls = [
        "https://delicias.dia.fi.upm.es/wiki/index.php/Special:AllPages",
        "https://delicias.dia.fi.upm.es/wiki/index.php?title=Special:AllPages&from=Licencias"
    ]

    # Obtener y guardar URLs
    scraper.scrape_and_save_urls(wiki_urls)
else:
    print("Error en el inicio de sesión")

# Cerrar el navegador
scraper.close() """
