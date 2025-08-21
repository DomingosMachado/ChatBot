import os
from dotenv import load_dotenv
from rag import add_document_to_rag, get_table

load_dotenv() 

def main():
    context_filepath = os.path.join("context", "infinitepay_solutions.md")
    
    context_session_id = "infinitepay-context"

    print("Checking if context is already loaded...")
    table = get_table()
    
    existing_docs = table.search().where(f"session_id = '{context_session_id}'", prefilter=True).limit(1).to_list()
    
    if existing_docs:
        print("Context has already been loaded into the vector database. Skipping.")
        return

    if not os.path.exists(context_filepath):
        print(f"Error: Context file not found at {context_filepath}")
        print("Please make sure you have created the file 'backend/context/infinitepay_solutions.md'")
        return

    print(f"Loading context from {context_filepath} into the vector store...")
    try:
        add_document_to_rag(context_filepath, context_session_id)
        print("Successfully loaded context into the vector store.")
    except Exception as e:
        print(f"An error occurred while loading the context: {e}")

if __name__ == "__main__":
    main()