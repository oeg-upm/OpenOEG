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

Por último, comprobar que Ollama se tiene instalado y operativo y que se tiene descargado los embedder y modelo que se pretenda usar.

### Uso

Para ejecutar el módulo de análisis ejecutar el script omnianalisis.py desde el directorio donde se haya clonado. Tardará unos minutos en ejecutarse y al finalizar habrá un mensaje de fin.

Para ejecutar el módulo de chat ejecutar el script chat.py desde el mismo directorio. Si el modo de evaluación no está activado, desde la terminal se le dará el prompt al usuario donde podrá escribir su pregunta, para enviarla simplemente pulsará enter. Para salir de este escribir como pregunta únicamente una q y pulsar enter.
Si el modo de evaluación está activado (eval: True) se buscará un csv en la carpeta 'textos' llamado 'goldstandard.csv', del que se extraerán las preguntas a evaluar. Luego se generará en la misma carpeta un txt con las métricas y un csv llamado 'respuestasModelo.csv' con las repeuestas generadas por si se quieren comprobar manualmente. Las métricas también serán impresas por pantalla cuando acabe la ejecución.


## NOTAS IMPORTANTES:

Si se quiere probar los resultados en español y luego en inglés se recomienda utilizar dos índices distintos para no mezclar, por eso también existen carpetas distintas dentro de nexo con ese propósito. Revisar en ese caso el indexname antes de ejecutar omnianalisis.

Es importante revisar siempre tanto al ejecutar chat como omnianalisis la opción new para asegurarse con cuál embedder se va a hacer y qué nexo se va a comprobar.

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
    new: False  # Escribir True para utilizar el embedder new (español), False para utilizar el embedder false (nomic)
    eval: True  # Escribir True para evaluar, False para no hacerlo, es decir, para hablar con el modelo
  paths:
    driver: "ruta/al/driver"  # Por defecto, geckodriver está en bin
    libreoffice: "ruta/a/libreoffice"
  embedder:
    old: "nombre del embedder en inglés (nomic)"
    new: "nombre del embedder en español (jina)"
  model:
    modelname: "nombre del modelo a usar en LM Studio"
```
