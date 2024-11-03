# ahí están los ppw (muchos)
# https://delicias.dia.fi.upm.es/wiki/index.php/Transparencias

# Todas las páginas
#
# https://delicias.dia.fi.upm.es/wiki/index.php/Special:AllPages



from selenium import webdriver #dependencia
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service #importar esto tambien TODO
from selenium.webdriver.firefox.options import Options
import time


firefox_options = Options()
firefox_options.add_argument("--headless") 
firefox_options.add_argument("--no-sandbox")
firefox_options.add_argument("--disable-dev-shm-usage")


geckodriver_path = 'C:/Users/Jaime Vázquez/AppData/Local/Programs/Python/Python313/geckodriver.exe'  # recordar estp TODO


service = Service(geckodriver_path)


driver = webdriver.Firefox(service=service, options=firefox_options)

# URL de inicio de sesión
login_url = "https://delicias.dia.fi.upm.es/wiki/index.php?title=Special:UserLogin&returnto=Main+Page&returntoquery="  # Cambia esto según tu MediaWiki
driver.get(login_url)


time.sleep(2)

# campos de usuario, contraseña y el botón de inicio de sesión
username_input = driver.find_element(By.ID, "wpName1")  
password_input = driver.find_element(By.ID, "wpPassword1") 
login_button = driver.find_element(By.ID, "wpLoginAttempt")  

# credenciales
username = "jaime.vrivera"
password = "9rScwwFGLZDNfGz"
username_input.send_keys(username)
password_input.send_keys(password)


login_button.click()


time.sleep(3)


if "Especial:Entrar" not in driver.current_url:
    print("Inicio de sesión exitoso")

    
    wiki_url = "https://delicias.dia.fi.upm.es/wiki/index.php?title=Special:AllPages&from=Licencias" #dos veces el link, el primero fue https://delicias.dia.fi.upm.es/wiki/index.php/Special:AllPages
    
    driver.get(wiki_url)

    
    time.sleep(2)

   
    page_links = driver.find_elements(By.CSS_SELECTOR, 'ul.mw-allpages-chunk li a')

    
    urls = [link.get_attribute('href') for link in page_links]

    
    print("Encontradas las siguientes URLs de las páginas:")
    for url in urls:
        print(url)

    """ # Opcionalmente, puedes navegar a cada URL y realizar scraping adicional
    for url in urls:
        driver.get(url)
        # Aquí puedes hacer scraping adicional si lo deseas
        print(f"Accediendo a: {url}")
        time.sleep(1) """

else:
    print("Error en el inicio de sesión")


driver.quit()
