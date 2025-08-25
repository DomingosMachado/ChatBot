import os
from dotenv import load_dotenv
from rag import add_document_to_rag, get_table

load_dotenv()

def main():
    context_dir = "context"
    context_session_id = "infinitepay-context"
    
    print("Checking if context is already loaded...")
    table = get_table()
    
    existing_docs = table.search().where(f"session_id = '{context_session_id}'", prefilter=True).limit(1).to_list()
    
    if existing_docs:
        print("Context already loaded. To reload, delete the lancedb folder first.")
        return
    
    # Walk through all subdirectories and load all .md files
    total_files = 0
    for root, dirs, files in os.walk(context_dir):
        for filename in files:
            if filename.endswith('.md'):
                filepath = os.path.join(root, filename)
                relative_path = os.path.relpath(filepath, context_dir)
                print(f"Loading {relative_path}...")
                try:
                    add_document_to_rag(filepath, context_session_id)
                    print(f"✅ Loaded {relative_path}")
                    total_files += 1
                except Exception as e:
                    print(f"❌ Error loading {relative_path}: {e}")
    
    print(f"\n✅ Successfully loaded {total_files} context files!")

if __name__ == "__main__":
    main()