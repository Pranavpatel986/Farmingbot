import os
import time
import sys
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()

# This function will automatically retry if Google sends a 429 error
@retry(
    stop=stop_after_attempt(10),
    wait=wait_exponential(multiplier=2, min=10, max=120),
    reraise=True
)
def add_batch_with_retry(vector_store, batch):
    vector_store.add_documents(batch)

def build_vector_db():
    print("🚀 Starting Ingestion for 'farmerbook.pdf'...")
    file_path = os.path.join("data", "farmerbook.pdf")
    
    if not os.path.exists(file_path):
        print(f"❌ ERROR: Could not find '{file_path}'.")
        return

    # 1. Load and Split
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(docs)
    print(f"📄 Found {len(docs)} pages. Split into {len(chunks)} chunks.")

    # 2. Initialize Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    # 3. Process in even smaller batches
    batch_size = 15  # Smaller batches reduce the "burst" pressure on the API
    print(f"📦 Indexing in batches of {batch_size} with auto-retry logic...")

    # Initialize the store with the first batch
    vector_store = Chroma.from_documents(
        documents=chunks[:batch_size],
        embedding=embeddings,
        persist_directory="chroma_db",
        collection_name="example_collection"
    )
    print(f"✅ Initial batch (0-{batch_size}) complete.")

    # 4. Loop through remaining chunks
    for i in range(batch_size, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        try:
            print(f"🔄 Processing {i} to {min(i + batch_size, len(chunks))}...")
            add_batch_with_retry(vector_store, batch)
            # Mandatory pause to stay under the 100 RPM limit
            time.sleep(10) 
        except Exception as e:
            print(f"\n❌ Permanent failure at chunk {i}: {e}")
            break

    print("\n🏁 SUCCESS: Database is ready for chatting!")

if __name__ == "__main__":
    build_vector_db()