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
embeddings_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

vector_store = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings_model,
    persist_directory=CHROMA_PATH,
)

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)

# Prompt with Citations Instruction
template = """
You are "FarmerBot", a scientific agricultural advisor. 
Use the following context to answer the question. 

Context: {context}
History: {history}
Question: {question}

Instructions:
1. If the answer is in the context, provide a detailed response.
2. Mention that the information is sourced from the "Farmer's Handbook".
3. If you don't know, suggest contacting a local agricultural extension office.

Answer:"""

prompt = ChatPromptTemplate.from_template(template)

def stream_response(message, history):
    # Retrieve top 4 most relevant chunks
    retriever = vector_store.as_retriever(search_kwargs={'k': 4})
    
    # RAG Chain
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
    # Landing Page Background
    gr.HTML(hero_html)
    
    # Floating Chat Widget
    with gr.Column(elem_id="floating_container"):
        gr.HTML('<div class="widget-header"><span>🌱</span> FarmerBot Assistant</div>')
        gr.ChatInterface(
            fn=stream_response,
            examples=["How to do soil testing?", "What is seed treatment?", "Explain weed management."],
        )

if __name__ == "__main__":
    import os
    
    # Get the port from Render's environment, or default to 10000
    server_port = int(os.environ.get("PORT", 10000))
    
    # Combine everything: Styling (from Block 1) + Networking (from Block 2)
    demo.launch(
        server_name="0.0.0.0",        # Required for Render
        server_port=server_port,       # Required for Render
        share=False,                   # Required for Render
        css=custom_css,                # Your custom design
        theme=gr.themes.Soft(primary_hue="emerald") # Your color theme
    )