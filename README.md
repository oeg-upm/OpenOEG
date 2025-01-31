# OpenOEG

## ¿Qué es OpenOEG?

OpenOEG es una herramienta que analiza todos las páginas de la OEGWiki y descarga y analiza todos los pdf, ptt y pttx de esta, guardando su información en una base de datos vectorial. Posteriormente integra un modelo de lenguaje que con técnicas RAG es capaz de responder preguntas sobre la wiki citando el material base. 

Consiste en dos módulos: el módulo de análisis y el módulo de chat. El módulo de chat consiste únicamente del script con el mismo nombre y el módulo de análisis consiste del resto de scripts.

## Guía de instalación y uso

Instalar requierements.txt.

Para Selenium, instalar el driver asociado al navegador que se pretende usar, siguiendo la guía de su página https://pypi.org/project/selenium/ y especificar la ruta del ejecutable en omnianalisis.py. El proyecto se ha probado en Firefox con geckodriver aunque debería funcionar con otros.

Modificar el fichero omnianalisis.py modificando las rutas necesarias, ajustando el fichero donde se encuentra el usuario y contraseña de la OEG y la ruta del fichero donde se guardarán todas las páginas 

Modificar el fichero pineconeupload.py y chat modificando las rutas necesarias, ajustando el fichero donde se encuentra el la llave de Pinecone, como la ruta del nexo. Modificar el nombre del index_name si se desea.
En caso de usar ollama revisar que se tiene instalado y que se tiene descagrado el embedder que se pretenda usar.
En caso de usar LMStudio asegurarse que a la hora de ejecutar se tiene el servidor local activado con el puerto y nombre del embedder correcto.

En chat actualizar
