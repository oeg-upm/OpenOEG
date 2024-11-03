

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

# Configurar opciones de Firefox
firefox_options = Options()
firefox_options.add_argument("--headless")  # Ejecutar en modo headless (sin abrir el navegador visualmente)
firefox_options.add_argument("--no-sandbox")
firefox_options.add_argument("--disable-dev-shm-usage")

# Ruta al GeckoDriver (modifica esta ruta según tu instalación)
geckodriver_path = 'C:/Users/Jaime Vázquez/AppData/Local/Programs/Python/Python313/geckodriver.exe'  # Cambia esto por la ruta donde tengas geckodriver

# Iniciar el servicio de GeckoDriver
service = Service(geckodriver_path)

# Iniciar el navegador Firefox con las opciones configuradas
driver = webdriver.Firefox(service=service, options=firefox_options)

# URL de la página especial "Todas las páginas" en MediaWiki
wiki_url = "https://en.wikipedia.org/wiki/Special:AllPages"

# Abre la página de "Todas las páginas"
driver.get(wiki_url)

# Esperar unos segundos para cargar la página completamente
time.sleep(2)

# Buscar todos los enlaces de la página
# Selecciona solo los enlaces dentro de la lista de páginas (puedes ajustar esto si la estructura cambia)
page_links = driver.find_elements(By.CSS_SELECTOR, 'ul.mw-allpages-chunk li a')

# Extraer las URLs de cada página
urls = [link.get_attribute('href') for link in page_links]

# Mostrar las URLs de las páginas
print("Encontradas las siguientes URLs de las páginas:")
for url in urls:
    print(url)

# Ahora, si quieres navegar a cada página y realizar acciones adicionales (opcional)
""" for url in urls:
    driver.get(url)
    # Aquí puedes hacer scraping adicional si lo deseas (como obtener el contenido de cada página)
    print(f"Accediendo a: {url}")
    time.sleep(1)  # Pausa para evitar ser bloqueado por el servidor
 """
# Cerrar el navegador una vez terminado
driver.quit()

