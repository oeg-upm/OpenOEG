# OpenOEG

## ¿Qué es OpenOEG?

OpenOEG es una herramienta que analiza todos las páginas de la OEGWiki y descarga y analiza todos los pdf, ptt y pttx de esta, guardando su información en una base de datos vectorial. Posteriormente integra un modelo de lenguaje que con técnicas RAG es capaz de responder preguntas sobre la wiki citando el material base. 

Consiste en dos módulos: el módulo de análisis y el módulo de chat. El módulo de chat consiste únicamente del script con el mismo nombre y el módulo de análisis consiste del resto de scripts.

## Guía de instalación y uso

### Instalación

Clonar el repositiorio.

Con pip instalar requirements.txt.

Crear en la carpeta textos tres ficheros llamados username_oeg.txt, password_oeg.txt y key_pinecone.txt donde estén el nombre de usuario del OEG, la contraseña del OEG y la clave del usuario en pinecone respectivamente.

Para Selenium, instalar el driver asociado al navegador que se pretende usar, siguiendo la guía de su página https://pypi.org/project/selenium/ y especificar la ruta del ejecutable en omnianalisis.py. El proyecto se ha probado en Firefox con geckodriver aunque debería funcionar con otros.

En caso de usar ollama revisar que se tiene instalado y que se tiene descargado el embedder que se pretenda usar.
En caso de usar LMStudio asegurarse se tiene instalado el embedder que se pretende usar y que a la hora de ejecutar cualquiera de los dos módulos se tiene el servidor local encendido con el puerto y nombre del embedder correcto. La versión de nomic usada viene por defecto en la instalación de LM Studio, si no descargar manualmente.

### Uso

Para ejecutar el módulo de análisis ejecutar el script omnianalisis.py desde el directorio donde se haya clonado. Tardará unos minutos en ejecutarse y al finalizar habrá un mensaje de fin.

Para ejecutar el módulo de chat ejecutar el script chat.py desde el mismo directorio. Desde la terminal se le dará el prompt al usuario donde podrá escribir su pregunta, para enviarla simplemente pulsará enter. Para salir de este escribir como pregunta únicamente una q y pulsar enter.

