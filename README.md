# OpenOEG

## ¿Qué es OpenOEG?

OpenOEG es una herramienta que analiza todos las páginas de la OEGWiki y descarga y analiza todos los pdf, ptt y pttx de esta, guardando su información en una base de datos vectorial. Posteriormente integra un modelo de lenguaje que con técnicas RAG es capaz de responder preguntas sobre la wiki citando el material base. 

Consiste en dos módulos: el módulo de análisis y el módulo de chat. El módulo de chat consiste únicamente del script con el mismo nombre y el módulo de análisis consiste del resto de scripts.

## Guía de instalación y uso

### Instalación

Es necesario tener una cuenta en Pinecone https://www.pinecone.io/ y anotar la key asociada a la cuenta que se puede obtener en https://docs.pinecone.io/guides/get-started/quickstart. Si tienes cuenta de Google puedes usarla para loggearte. No hace falta la versión de pago de Pinecone, con la versión gratis es suficiente. 

Clonar el repositiorio.

Con pip instalar requirements.txt.

Modificar el fichero config.yaml de la manera que se indica al final.

Para Selenium, instalar el driver asociado al navegador que se pretende usar, siguiendo la guía de su página https://pypi.org/project/selenium/ y especificar la ruta del ejecutable en el fichero config. El proyecto se ha probado en Firefox con geckodriver aunque debería funcionar con otros.

Descargar e instalar LibreOffice https://es.libreoffice.org/descarga/libreoffice/ usando la versión correspondiente a su sistema operativo y luego especificar la ruta a soffice (en la versión de windows sería al fichero soffice.exe).

En caso de usar Ollama revisar que se tiene instalado y que se tiene descargado el embedder que se pretenda usar.
En caso de usar LMStudio asegurarse se tiene instalado el embedder que se pretende usar o el modelo de lenguaje y que a la hora de ejecutar cualquiera de los dos módulos se tiene el servidor local encendido con el puerto y nombre del embedder correcto. 

### Uso

Para ejecutar el módulo de análisis ejecutar el script omnianalisis.py desde el directorio donde se haya clonado. Tardará unos minutos en ejecutarse y al finalizar habrá un mensaje de fin.

Para ejecutar el módulo de chat ejecutar el script chat.py desde el mismo directorio. Desde la terminal se le dará el prompt al usuario donde podrá escribir su pregunta, para enviarla simplemente pulsará enter. Para salir de este escribir como pregunta únicamente una q y pulsar enter.


## NOTAS IMPORTANTES:

En la versión actual PARA INSERTAR DATOS EN PINECONE (es decir, el script de omnianalisis.py):

La versión 'old' usa el embedder por medio de LMStudio
La versión 'new' usa el embedder por medio de Ollama

Para HACER CONSULTAS (es decir, el script de chat.py):

Se puede usar tanto Ollama como LMStudio. Tener en cuenta la opción 'new' para la elección.

El fichero yaml llamado config se presenta a continuación:

```yaml
config:
  credentials:
    oeg:
      username: "usuario de la OEG"
      password: "contraseña de la OEG"
    pinecone:
      key: "key de Pinecone"
      indexname: "nombre del índice de Pinecone"  # Solo se permiten letras minúsculas y guiones (-)
  options:
    new: False  # Escribir True para la versión de Ollama, False para la versión de LM Studio
    eval: True  # Escribir True para evaluar, False para no hacerlo
  paths:
    driver: "ruta/al/driver"  # Por defecto, geckodriver está en bin
    libreoffice: "ruta/a/libreoffice"
  embedder:
    old: "nombre del embedder de LMStudio (para probar con embedders en inglés)"
    new: "nombre del embedder de Ollama (para probar con embedders en español)"
  model:
    modelname: "nombre del modelo a usar en LM Studio"
    modelnamellama: "nombre del modelo a usar en Ollama"
    host: "http://localhost:1234/v1"  # Dirección del modelo (por defecto en versión local)
    api_key: "lm-studio"  # Si el modelo requiere autenticación (por defecto lm-studio en local)
```