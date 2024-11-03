from analisisppt import PPTXProcessor
from pdfanalysis import PDFProcessor
from ppttopdf import PPTtoPDFConverter

#Teniendo todas las descargas de la página sube todo a pinecone
#Para cambiar la base de datos, ver el fichero de pineconeupload

documents_path = "C:/Users/Jaime Vázquez/Documents/Python/tfg/ptts2/"


miPDFconverter = PPTtoPDFConverter(documents_path)
miPPTXProcessor= PPTXProcessor(documents_path)
miPDFProcessor= PDFProcessor(documents_path)

miPDFconverter.convert_to_pdf()
miPDFconverter.close()

miPPTXProcessor.analyze_and_upload()
miPDFProcessor.analyze_and_upload()