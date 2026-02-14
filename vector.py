from langchain_community.document_loaders import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

def create_vector_store():
    """Create vector store with HuggingFace embeddings (no API key needed!)"""
    
    # Load heart medicine dataset
    loader = CSVLoader(
        file_path="heart_medicine_dataset.csv",
        encoding="utf-8",
        csv_args={'delimiter': ','}
    )
    
    documents = loader.load()
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=80
    )
    splits = text_splitter.split_documents(documents)
    
    # Create embeddings using HuggingFace (FREE - no API key needed!)
    # Using a lightweight model that works well
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    
    # Create FAISS vector store
    vectorstore = FAISS.from_documents(
        documents=splits,
        embedding=embeddings
    )
    
    # Save vector store for reuse
    vectorstore.save_local("faiss_index")
    
    print("✅ Heart Medicine Vector Store created successfully!")
    print(f"📊 Total conditions loaded: {len(documents)}")
    print(f"📦 Total chunks created: {len(splits)}")
    
    return vectorstore

def load_vector_store():
    """Load existing vector store or create new one"""
    
    # Check if vector store already exists
    if os.path.exists("faiss_index"):
        print("📂 Loading existing vector store...")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        vectorstore = FAISS.load_local(
            "faiss_index", 
            embeddings,
            allow_dangerous_deserialization=True
        )
        print("✅ Vector store loaded!")
    else:
        print("🔨 Creating new vector store...")
        vectorstore = create_vector_store()
    
    return vectorstore

# Initialize retriever
vectorstore = load_vector_store()
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

if __name__ == "__main__":
    # Test retriever
    test_query = "chest pain"
    results = retriever.invoke(test_query)
    print(f"\n🧪 Test query: '{test_query}'")
    print(f"📋 Found {len(results)} relevant documents")
