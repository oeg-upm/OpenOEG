import os
from openai import OpenAI
import json
import re
from time import time,sleep
from uuid import uuid4
import datetime
import yaml
import ollama
from pinecone import Pinecone, ServerlessSpec


with open('config.yaml', 'r') as yaml_file:
    config = yaml.safe_load(yaml_file)

new = config["config"]["options"]["new"]
test = config["config"]["options"]["eval"]

if new:
    mi_model =  config["config"]["model"]["modelnamellama"]
    mi_model_emb = config["config"]["embedder"]["new"]
else:
    mi_model =  config["config"]["model"]["modelname"]
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


# Revisar esto https://huggingface.co/nomic-ai/nomic-embed-text-v1.5
# para RAG 
 
def get_embedding(text, rol):
   text = text.replace("\n", " ") 
   
   # las de sistema search_document:
   # las de usuario search_query:
   if new:
        text = text.replace("\n", " ")
            
        if rol == "USER":
            text= "search_query: "+text
                
        elif rol == "SYSTEM":
            text = "search_document: "+text
                
        else: #ASSISTANT
            text = text
        return ollama.embeddings(model=mi_model_emb, prompt=text)["embedding"]
    
   else:
        if rol == "USER":
            return client.embeddings.create(input = ["search_query: "+text], model=mi_model_emb).data[0].embedding 
                
        elif rol == "SYSTEM":
            return client.embeddings.create(input = ["search_document: "+text], model=mi_model_emb).data[0].embedding 
            
        else: #ASSISTANT
            return client.embeddings.create(input = [text], model=mi_model_emb).data[0].embedding 

client = OpenAI(
    
    base_url=config["config"]["model"]["host"],
    api_key=config["config"]["model"]["api_key"]
)


def text_completion(prompt, engine=mi_model):
    max_retry = 5
    retry = 0
    #p#rompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
    
    #print("\n soy la prompt ey" + prompt +"\n")
    
    while True:
        try:
                
            if new:
                response = ollama.chat(mi_model, messages=[{"role": "user", "content": prompt}])
                
                text = response["message"]["content"]
                text = re.sub('[\r\n]+', '\n', text)
                text = re.sub('[\t ]+', ' ', text)                
            else:
                response = client.chat.completions.create(
                                        messages=[
                                            {
                                                "role": "user",
                                                "content": prompt,
                                            }
                                        ],
                                        model=engine,
                                    )
                
                
                text = response.choices[0].message.content
                    #text = response['choices'][0]['text'].strip()
                    #print("\n"+text+"\n")
                text = re.sub('[\r\n]+', '\n', text)
                text = re.sub('[\t ]+', ' ', text)
                    #filename = '%s_log.txt' % time()
                    #if not os.path.exists('./textos/logs'):
                    #    os.makedirs('./textos/logs')
                    #save_file('./textos/logs/%s' % filename, prompt + '\n\n==========\n\n' + text)
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


if __name__ == '__main__':
    convo_length = 2 # se puede cambiar
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
    
    while True:
        #### get user input, save it, vectorize it, save to pinecone
        payload = list()
        a = input('\n\nUSER: ')
        
        if (a == "q"):
            #save_json('./nexo/%s.json' % unique_id, metadata)
            break
        
        
        
        timestamp = time()
        timestring = timestamp_to_datetime(timestamp)
        message = '%s: %s - %s' % ('USER', timestring, a)
       
       
        vector = get_embedding(message, "USER")
        #unique_id = str(uuid4())
        #metadata = {'speaker': 'USER', 'time': timestamp, 'message': message, 'timestring': timestring, 'uuid': unique_id}
        #save_json('./nexo2/%s.json' % unique_id, metadata)
        #payload.append((unique_id, vector))
        #### search for relevant messages, and generate a response
        results = index.query(vector=vector, top_k=convo_length)
        wiki_data = check_nexo(results)  # results should be a DICT with 'matches' which is a LIST of DICTS, with 'id'
        
        
        
        #filename = unique_conv_id+'_log.txt' 
        if not os.path.exists('./textos/logs'):
            os.makedirs('./textos/logs')
        
        #prev_conv = open_file('./textos/logs/%s' % filename)
        #save_file('./textos/logs/%s' % filename, prev_conv+"\n"+message)
        
        prev_conv = open_file('./textos/logs/%s' % filename)
        
        
        #print("\n\nSoy las conversacion previa, a ver que hay aquí \n \n")
        #print(prev_conv)
        #print("\n \n")
        
        #print("\n\nSoy los datos, a ver que hay aquí \n \n")
        #print(wiki_data)
        #print("\n \n") 
       
        
        prompt = open_file('./textos/contexto.txt').replace('<<DATOS>>', wiki_data).replace('<<CONVERSACIÓN>>', prev_conv).replace('<<MENSAJE>>', a) #puede que sea demasiado largo, mirar

        #print(prompt)
        
        
        #### generate response, vectorize, save, etc
        output = text_completion(prompt) #prompt
        timestamp = time()
        timestring = timestamp_to_datetime(timestamp)
        
        messageBot = '%s: %s - %s' % ('ABIGAIL', timestring, output)
        
        print('\n\nABIGAIL: %s' % output) 
        
        if test:
            print("\n ¿Es la respuesta buena o no? Responder con Y/N  (si/no)") 
            res = input('\n\nUSER (Y/N): ')

        if test:
            
            save_file('./textos/logs/%s' % filename, prev_conv+"\n"+message+"\n"+messageBot+"\n La respuesta es "+res)
            
        else:
            save_file('./textos/logs/%s' % filename, prev_conv+"\n"+message+"\n"+messageBot)
        #message = output
        #vector = get_embedding(message, "ASSISTANT")
        #unique_id = str(uuid4())
        #metadata = {'speaker': 'ABIGAIL', 'time': timestamp, 'message': message, 'timestring': timestring, 'uuid': unique_id}
        #save_json('./nexo2/%s.json' % unique_id, metadata)
        #payload.append((unique_id, vector))
        #index.upsert(payload)
        