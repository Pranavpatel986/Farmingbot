import os
import gradio as gr
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Import Design
from ui_config import custom_css, hero_html

load_dotenv()

# --- BACKEND SETUP ---
CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "example_collection"

# 1. Initialize Gemini Embeddings
embeddings_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# 2. Connect to Chroma (Ensure this folder exists in your GitHub repo)
vector_store = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings_model,
    persist_directory=CHROMA_PATH,
)

# 3. Use Gemini 1.5 Flash (Better quota for Free Tier)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1)

template = """
You are "FarmerBot", a scientific agricultural advisor. 
Use the following context to answer the question. 

Context: {context}
History: {history}
Question: {question}

Instructions:
1. Provide a detailed response based on the context.
2. Mention that the information is sourced from the "Farmer's Handbook".
3. If the answer is not in the context, suggest contacting a local agricultural extension office.

Answer:"""

prompt = ChatPromptTemplate.from_template(template)

def stream_response(message, history):
    # Retrieve top 2 chunks (Lower 'k' saves memory on Render Free Tier)
    retriever = vector_store.as_retriever(search_kwargs={'k': 2})
    
    rag_chain = (
        {
            "context": retriever | (lambda docs: "\n\n".join(d.page_content for d in docs)), 
            "question": RunnablePassthrough(), 
            "history": lambda x: history
        }
        | prompt 
        | llm 
        | StrOutputParser()
    )

    partial_message = ""
    for chunk in rag_chain.stream(message):
        partial_message += chunk
        yield partial_message

# --- UI CONSTRUCTION ---
with gr.Blocks(title="FarmerBot AI Portal") as demo:
    gr.HTML(hero_html)
    
    with gr.Column(elem_id="floating_container"):
        gr.HTML('<div class="widget-header"><span>🌱</span> FarmerBot Assistant</div>')
        gr.ChatInterface(
            fn=stream_response,
            examples=["How to do soil testing?", "What is seed treatment?", "Explain weed management."],
        )

if __name__ == "__main__":
    # RENDER FIX: Bind to 0.0.0.0 and use the PORT environment variable
    import os
    server_port = int(os.environ.get("PORT", 10000))
    
    demo.launch(
        server_name="0.0.0.0", 
        server_port=server_port,
        share=False  # Must be False for cloud deployments
    )