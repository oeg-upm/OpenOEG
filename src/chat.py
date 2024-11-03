import os
from openai import OpenAI
import json
import re
from time import time,sleep
from uuid import uuid4
import datetime
from pinecone import Pinecone, ServerlessSpec


mi_model = "meta-llama-3.1-8b-instruct"
mi_model_emb = "nomic-embed-text-v1.5"
index_name = "oegdb-ppt"

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_file(filepath, content):
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

#TODO 
# Revisar esto https://huggingface.co/nomic-ai/nomic-embed-text-v1.5
# para RAG 
 
def get_embedding(text, rol):
   text = text.replace("\n", " ") 
   
   # las de sistema search_document:
   # las de usuario search_query:
   
   if rol == "USER":
        return client.embeddings.create(input = ["search_query: "+text], model=mi_model_emb).data[0].embedding 
    
   elif rol == "SYSTEM":
       return client.embeddings.create(input = ["search_document: "+text], model=mi_model_emb).data[0].embedding 
   
   else: #ASSISTANT
        return client.embeddings.create(input = [text], model=mi_model_emb).data[0].embedding 

client = OpenAI(
    # This is the default and can be omitted
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)


def text_completion(prompt, engine=mi_model, stop=['USER:', 'ABIGAIL:']):
    max_retry = 5
    retry = 0
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
    
    #print("\n soy la prompt ey" + prompt +"\n")
    
    while True:
        try:
            response = client.chat.completions.create(
                                messages=[
                                    {
                                        "role": "user",
                                        "content": prompt,
                                    }
                                ],
                                model=mi_model,
                            )
            
            
            text = response.choices[0].message.content
            #text = response['choices'][0]['text'].strip()
            #print("\n"+text+"\n")
            text = re.sub('[\r\n]+', '\n', text)
            text = re.sub('[\t ]+', ' ', text)
            filename = '%s_log.txt' % time()
            if not os.path.exists('./tfg/textos/logs'):
                os.makedirs('./tfg/textos/logs')
            save_file('./tfg/textos/logs/%s' % filename, prompt + '\n\n==========\n\n' + text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "Model error: %s" % oops
            print('Error communicating with model:', oops)
            sleep(1)


def load_conversation(results): #esta es la clave TODO
    result = list()
    for m in results['matches']:
        try:
            info = load_json('./tfg/nexo2/%s.json' % m['id']) #TODO cambie por nexo2
            result.append(info)
        except:
            print("Parece que " + './tfg/nexo2/%s.json' % m['id'] + " no esta" )
            continue
    #ordered = sorted(result, key=lambda d: d['time'], reverse=False)  # sort them all chronologically
    messages = [i['message'] for i in result]
    return '\n'.join(messages).strip()



#TODO https://delicias.dia.fi.upm.es/wiki/index.php/Charlas


if __name__ == '__main__':
    convo_length = 5
    #openai.api_key = open_file('./tfg/openaiapikey.txt')
    
    pc = Pinecone(
        api_key=open_file('./tfg/key_pinecone.txt')
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
    save_file('./tfg/textos/logs/%s' % filename, prev_conv)
    
    # index.upsert -> echarle un ojo
    
    while True:
        #### get user input, save it, vectorize it, save to pinecone
        payload = list()
        a = input('\n\nUSER: ')
        
        if (a == "q"):
            #save_json('./tfg/nexo/%s.json' % unique_id, metadata)
            break
        
        
        
        timestamp = time()
        timestring = timestamp_to_datetime(timestamp)
        message = '%s: %s - %s' % ('USER', timestring, a)
       
       
        vector = get_embedding(message, "USER")
        #unique_id = str(uuid4())
        #metadata = {'speaker': 'USER', 'time': timestamp, 'message': message, 'timestring': timestring, 'uuid': unique_id}
        #save_json('./tfg/nexo2/%s.json' % unique_id, metadata)
        #payload.append((unique_id, vector))
        #### search for relevant messages, and generate a response
        results = index.query(vector=vector, top_k=convo_length)
        wiki_data = load_conversation(results)  # results should be a DICT with 'matches' which is a LIST of DICTS, with 'id'
        
        #TODO ver que demonios debería ser esto fada895b-16dc-475e-8cce-f2055f6f0d08.json
        
        
        
        filename = unique_conv_id+'_log.txt' 
        if not os.path.exists('./tfg/textos/logs'):
            os.makedirs('./tfg/textos/logs')
        
        prev_conv = open_file('./tfg/textos/logs/%s' % filename)
        save_file('./tfg/textos/logs/%s' % filename, prev_conv+"\n"+message)
        
        prev_conv = open_file('./tfg/textos/logs/%s' % filename)
        
        
        print("\n\nSoy las conversacion previa, a ver que hay aquí \n \n")
        print(prev_conv)
        print("\n \n")
        
        print("\n\nSoy los datos, a ver que hay aquí \n \n")
        print(wiki_data)
        print("\n \n")
        
        prompt = open_file('./tfg/textos/contexto.txt').replace('<<DATOS>>', wiki_data).replace('<<CONVERSACIÓN>>', prev_conv).replace('<<MENSAJE>>', a)
        #### generate response, vectorize, save, etc
        output = text_completion(prompt) #prompt
        timestamp = time()
        timestring = timestamp_to_datetime(timestamp)
        
        message = '%s: %s - %s' % ('ABIGAIL', timestring, output)
        
        
        save_file('./tfg/textos/logs/%s' % filename, prev_conv+"\n"+message)
        
        
        #message = output
        vector = get_embedding(message, "ASSISTANT")
        #unique_id = str(uuid4())
        #metadata = {'speaker': 'ABIGAIL', 'time': timestamp, 'message': message, 'timestring': timestring, 'uuid': unique_id}
        #save_json('./tfg/nexo2/%s.json' % unique_id, metadata)
        #payload.append((unique_id, vector))
        #index.upsert(payload)
        print('\n\nABIGAIL: %s' % output) 