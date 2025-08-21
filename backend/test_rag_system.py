import os
import sys
sys.path.append('.')

from rag import query_rag, get_table

def load_context_fixed():
    """Fixed context loading function"""
    from rag import add_document_to_rag
    
    # Use the correct filename
    context_filepath = os.path.join("context", "infinitypay_solutions.md")
    context_session_id = "infinitepay-context"
    
    if not os.path.exists(context_filepath):
        print(f"❌ Context file not found at {context_filepath}")
        # Check what files actually exist
        context_dir = "context"
        if os.path.exists(context_dir):
            files = os.listdir(context_dir)
            print(f"Files found in context directory: {files}")
            # Try to use the first .md file found
            md_files = [f for f in files if f.endswith('.md')]
            if md_files:
                context_filepath = os.path.join(context_dir, md_files[0])
                print(f"Using file: {context_filepath}")
            else:
                return False
        else:
            print(f"Context directory '{context_dir}' not found!")
            return False
    
    try:
        add_document_to_rag(context_filepath, context_session_id)
        print(f"✅ Successfully loaded context from {context_filepath}")
        return True
    except Exception as e:
        print(f"❌ Error loading context: {e}")
        return False

def test_rag_system():
    print("=== Testing RAG System ===")
    
    # 1. Check if context is loaded
    table = get_table()
    results = table.search().where("session_id = 'infinitepay-context'", prefilter=True).limit(5).to_list()
    
    print(f"Number of documents in vector store: {len(results)}")
    
    if len(results) == 0:
        print("❌ No context loaded! Loading now...")
        success = load_context_fixed()
        if success:
            results = table.search().where("session_id = 'infinitepay-context'", prefilter=True).limit(5).to_list()
            print(f"After loading: {len(results)} documents")
        else:
            print("❌ Failed to load context!")
            return False
    
    # 2. Test document content
    if results:
        print("\n=== Sample Document Content ===")
        print(f"First document snippet: {results[0]['text'][:200]}...")
    
    # 3. Test retrieval with sample questions
    test_questions = [
        "O que é a maquininha Smart?",
        "Como funciona o InfiniteTap?", 
        "Quais são as taxas da InfinitePay?",
        "Como faço para receber na hora?"
    ]
    
    print("\n=== Testing Question Retrieval ===")
    for question in test_questions:
        print(f"\nQuestion: {question}")
        context = query_rag(question, "infinitepay-context")
        if context:
            print(f"✅ Context found: {len(context)} characters")
            print(f"Preview: {context[:150]}...")
        else:
            print("❌ No context retrieved!")
    
    return len(results) > 0

if __name__ == "__main__":
    test_rag_system()