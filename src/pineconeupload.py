from pinecone import Pinecone, ServerlessSpec
import ollama
from uuid import uuid4
import json
import os
import yaml

'''Sube los ficheros a pinecone y guarda el json para referenciarlos más tarde'''


with open('config.yaml', 'r') as yaml_file:
    config = yaml.safe_load(yaml_file)




new = config["config"]["options"]["new"]


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

def save_json(filepath, payload):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        json.dump(payload, outfile, ensure_ascii=False, sort_keys=True, indent=2)

class PineconeUploader:
    def __init__(self):
        
        
    
        self.index_name = config["config"]["credentials"]["pinecone"]["indexname"]

        if new:
            self.nexo_path = "./nexo/jina/"
        else:
            self.nexo_path = "./nexo/nomic/"
        os.makedirs(self.nexo_path, exist_ok=True)
        self.pc = Pinecone(api_key = config["config"]["credentials"]["pinecone"]["key"])
        
        
        self.index = self._setup_pinecone_index()
        
    
    
    def get_embedding(self, text, rol):
           
            text = text.replace("\n", " ")
            
            if rol == "USER":
                text= "search_query: "+text
                
            elif rol == "SYSTEM":
                text = "search_document: "+text
                
            else: #ASSISTANT
                text = text
                
            if new:
            
                return ollama.embeddings(model=config["config"]["embedder"]["new"], prompt=text)["embedding"]
            else:
                return ollama.embeddings(model=config["config"]["embedder"]["old"], prompt=text)["embedding"]
    
    def _setup_pinecone_index(self):
        """Crea el índice en Pinecone si no existe, y lo devuelve."""
        
        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                    name=self.index_name,
                    dimension=768,
                    metric="euclidean",
                    spec=ServerlessSpec(cloud='aws', region='us-east-1')
                )
            
        return self.pc.Index(self.index_name)
    
    
    def upload_text(self, text, rol):
        
        
        unique_id = str(uuid4())
        vector = self.get_embedding(text, rol)
        payload = [(unique_id, vector)]
        
        self.index.upsert(payload)
        
        
        message = '%s: %s' % (rol, text)
        metadata = {'speaker': rol, 'message': message, 'uuid': unique_id}
        save_json(self.nexo_path+'%s.json' % unique_id, metadata)



    def bulk_upload(self, texts, rol): #subir varios de golpe, más eficiente en principio
        
        payload = []
        
        for text in texts:
            
            unique_id = str(uuid4())
            vector = self.get_embedding(text, rol)
            
            payload.append((unique_id, vector))
            
            message = '%s: %s' % ('SYSTEM', text)
            metadata = {'speaker': 'SYSTEM', 'message': message, 'uuid': unique_id}
            save_json(self.nexo_path+'%s.json' % unique_id, metadata)
        
        #print(len(payload))
        self.index.upsert(payload)

        