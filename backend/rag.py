# domingosmachado/chatbot/ChatBot-c52a09916732c591151116fd44bf41bbdf5f54e5/backend/rag.py
import lancedb
from unstructured.partition.auto import partition
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

db = lancedb.connect("./lancedb")
table_name = "documents_google"

def get_table():
    if table_name in db.table_names():
        return db.open_table(table_name)
    
    return db.create_table(
        table_name,
        data=[{"vector": [0.0] * 768, "text": "init", "session_id": "init"}],
        mode="overwrite"
    )

def add_document_to_rag(filepath: str, session_id: str):
    table = get_table()
    elements = partition(filename=filepath)
    
    docs_to_add = []
    for el in elements:
        text = el.text
        result = genai.embed_content(model="models/text-embedding-004", content=text)
        embedding = result['embedding']
        docs_to_add.append({"vector": embedding, "text": text, "session_id": session_id})
    
    if docs_to_add:
        table.add(docs_to_add)

def query_rag(query: str, session_id: str) -> str:
    table = get_table()
    result = genai.embed_content(model="models/text-embedding-004", content=query)
    query_vector = result['embedding']

    results = table.search(query_vector).where(f"session_id = '{session_id}'", prefilter=True).limit(3).to_list()
    
    context = "\n".join([result['text'] for result in results])
    return context