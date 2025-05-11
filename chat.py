import os
import json
import re
from time import time,sleep
from uuid import uuid4
import datetime
import yaml
import ollama
from pinecone import Pinecone, ServerlessSpec
import csv
from src.evaluador import evaluar_respuestas


with open('config.yaml', 'r') as yaml_file: #TODO
    config = yaml.safe_load(yaml_file)

new = config["config"]["options"]["new"]
eval = config["config"]["options"]["eval"]
mi_model =  config["config"]["model"]["modelname"]

if new:
    
    mi_model_emb = config["config"]["embedder"]["new"]
else:
    
    mi_model_emb = config["config"]["embedder"]["old"]
index_name = config["config"]["credentials"]["pinecone"]["indexname"]


if new:
    mi_nexo_path = "./nexo/jina/"
else:
    mi_nexo_path = "./nexo/nomic/"

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_file(filepath, content):
    #s.makedirs(os.path.dirname(filepath), exist_ok=True) no cambies esto, revisa el directorio antes
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return json.load(infile)


def save_json(filepath, payload):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        json.dump(payload, outfile, ensure_ascii=False, sort_keys=True, indent=2)


def timestamp_to_datetime(unix_time):
    return datetime.datetime.fromtimestamp(unix_time).strftime("%A, %B %d, %Y at %I:%M%p %Z")

def guardar_texto(textos, ruta_csv):
    with open(ruta_csv, mode='w', newline='', encoding='utf-8') as archivo:
        writer = csv.writer(archivo)
        for texto in textos:
            writer.writerow([texto])
            
# Revisar esto https://huggingface.co/nomic-ai/nomic-embed-text-v1.5
# para RAG 
 
def get_embedding(text, rol):
   text = text.replace("\n", " ") 
   
   # las de sistema search_document:
   # las de usuario search_query:
   
   text = text.replace("\n", " ")
        
   if rol == "USER":
       text= "search_query: "+text
           
   elif rol == "SYSTEM":
       text = "search_document: "+text
           
   else: #ASSISTANT
       text = text
       
   return ollama.embeddings(model=mi_model_emb, prompt=text)["embedding"]


def extraer_ultimos_mensajes(conversacion, n=2):
    # Divide la conversación en bloques de mensajes (USER o ABIGAIL)
    if not conversacion.strip():
        return ''
    
    bloques = re.findall(r'(USER:.*?)(?=USER:|$)', conversacion, re.DOTALL)

    # También incluye posibles respuestas de ABIGAIL después de cada USER
    resultados = []
    for bloque in bloques:
        respuesta = re.search(r'(ABIGAIL:.*?)(?=USER:|$)', conversacion[conversacion.find(bloque) + len(bloque):], re.DOTALL)
        if respuesta:
            resultados.append(bloque.strip() + '\n' + respuesta.group().strip())
    
    # Devuelve los últimos n mensajes
    return '\n\n'.join(resultados[-n:])

def text_completion(prompt, mi_model, system_prompt):
    max_retry = 5
    retry = 0
    #p#rompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
    
    #print("\n soy la prompt ey" + prompt +"\n")
    
    while True:
        try:
            
            
            
            response = ollama.chat(mi_model, messages=[{
                'role': 'system',
                'content': system_prompt,
            },
                                                       
            {"role": "user", "content": prompt}])
            
            text = response["message"]["content"]
            text = re.sub('[\r\n]+', '\n', text)
            text = re.sub('[\t ]+', ' ', text)                
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "Model error: %s" % oops
            print('Error communicating with model:', oops)
            sleep(1)


def check_nexo(results):
    result = list()
    for m in results['matches']:
        try:
            info = load_json(mi_nexo_path + '%s.json' % m['id']) #TODO cambie por nexo2
            result.append(info)
        except:
            print("Parece que " + mi_nexo_path+'%s.json' % m['id'] + " no esta" )
            continue
    #ordered = sorted(result, key=lambda d: d['time'], reverse=False)  # sort them all chronologically
    messages = [i['message'] for i in result]
    return '\n'.join(messages).strip()



#TODO https://delicias.dia.fi.upm.es/wiki/index.php/Charlas


def evaluate(a):
    

        timestamp = time()
        timestring = timestamp_to_datetime(timestamp)
        message = '%s: %s - %s' % ('USER', timestring, a)
    
    
        vector = get_embedding(a, "USER")
        results = index.query(vector=vector, top_k=vectores_a_extraer)
        wiki_data = check_nexo(results)  # results should be a DICT with 'matches' which is a LIST of DICTS, with 'id'
        
        
        
        #filename = unique_conv_id+'_log.txt' 
        if not os.path.exists('./textos/logs'):
            os.makedirs('./textos/logs')
        
        #prev_conv = open_file('./textos/logs/%s' % filename)
        #save_file('./textos/logs/%s' % filename, prev_conv+"\n"+message)
        
        prev_conv = open_file('./textos/logs/%s' % filename)
        
        #ultimas = extraer_ultimos_mensajes(prev_conv, n=1)
        
        #ultimas = ""
        #print("\n\nSoy las conversacion previa, a ver que hay aquí \n \n")
        #print(ultimas)
        #print("\n \n")
        
        print("\n\nSoy los datos, a ver que hay aquí \n \n")
        print(wiki_data)
        print("\n \n") 
    
        
        #prompt = open_file('./textos/contexto.txt').replace('<<DATOS>>', wiki_data).replace('<<CONVERSACIÓN>>', ultimas).replace('<<MENSAJE>>', a) #puede que sea demasiado largo, mirar
        #print(prompt)
        sys_context = open_file('./textos/contexto.txt')

        
        output = text_completion(wiki_data + "\n\nA continuación darás una respuesta a la última pregunta formulada:\n\n" +a, mi_model, sys_context) #prompt
        timestamp = time()
        timestring = timestamp_to_datetime(timestamp)
        
        messageBot = '%s: %s - %s' % ('ABIGAIL', timestring, output)
        
        save_file('./textos/logs/%s' % filename, prev_conv+"\n"+message+"\n"+messageBot)

        return output

if __name__ == '__main__':
    vectores_a_extraer = 2 # se puede cambiar
    #openai.api_key = open_file('./openaiapikey.txt')
    
    pc = Pinecone(
        api_key=config["config"]["credentials"]["pinecone"]["key"]
    )
    # index_name = "mispruebas-index"
    # Now do stuff
    if index_name not in pc.list_indexes().names():
     pc.create_index(
        name=index_name,
        dimension=768,
        metric="euclidean",
        spec=ServerlessSpec(
            cloud='aws', 
            region='us-east-1'
        ) 
    ) 
    
    
    #pinecone.init(api_key=, environment='us-east1-gcp')
   
    index = pc.Index(index_name)
    unique_conv_id = str(uuid4())
    prev_conv = ""
    filename = unique_conv_id+'_log.txt' 
    
   #rint("Voy a guardar")
    save_file('./textos/logs/%s' % filename, prev_conv)
    #rint("He fgardar")
    
        # index.upsert -> echarle un ojo
    
    
    if eval:
        
        csv_file_path = './textos/goldstandard.csv'


        preguntas = []
        respuestasCSV = []
        respuestasModelo = []

        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)

            for row in reader:
                
                joined_row = ' '.join(row)
                
                if ';' in joined_row:
                    pregunta, respuesta = joined_row.split(';', 1)
                    preguntas.append(pregunta.strip())
                    respuestasCSV.append(respuesta.strip())
                else:
                    
                    preguntas.append(joined_row.strip())
                    respuestasCSV.append("")

        #hacemos preguntas
        
        #print("PREGUNTAS:")
        #for q in preguntas:
        #    print("-",q)
        #
        #print("\nRESPUESTAS:")
        #for r in respuestasCSV:
        #    print("-", r)
        #
        
        for pregunta in preguntas:
            
            respuestasModelo.append(evaluate(pregunta))
            print("Pregunta "+ pregunta+  " ejecutada")
        
        guardar_texto(respuestasModelo, './textos/respuestasModelo.csv')
        
        res = evaluar_respuestas(respuestasCSV=respuestasCSV,respuestasLLM=respuestasModelo)

        with open("./textos/metrics.txt", 'w', encoding='utf-8') as archivo:
            for clave, valor in res.items():
                archivo.write(f"{clave}: {valor}\n")
        
        print("\n Se ha generado CSV con las respuetas del modelo y los resultados son: \n")
        for key, value in res.items():
            print(f"{key}: {value}")

        
        
        
        
        
    else:
        while True:
            
            payload = list()
            a = input('\n\nUSER: ')
            
            if (a == "q"):
                #save_json('./nexo/%s.json' % unique_id, metadata)
                break
            
            
            print('\n\nABIGAIL: %s' % evaluate(a)) 
            
            #message = output
            #vector = get_embedding(message, "ASSISTANT")
            #unique_id = str(uuid4())
            #metadata = {'speaker': 'ABIGAIL', 'time': timestamp, 'message': message, 'timestring': timestring, 'uuid': unique_id}
            #save_json('./nexo2/%s.json' % unique_id, metadata)
            #payload.append((unique_id, vector))
            #index.upsert(payload)
            