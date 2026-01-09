import os
import gradio as gr
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Load environment variables
load_dotenv()

# Configuration
CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "example_collection"

# 1. FIXED: Initialize Gemini Embeddings to match your ingestion script
# Using gemini-embedding-001 to solve the 3072 dimension error
embeddings_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# 2. Connect to the Chroma Vector Store
vector_store = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings_model,
    persist_directory=CHROMA_PATH,
)

# 3. Initialize the Gemini 2.5 Flash Model
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)

# 4. Define the Modern RAG Prompt Template
template = """
You are a helpful assistant. Use ONLY the following pieces of context to answer the question. 
If you don't know the answer based on the context, just say you don't know. 
Do not use your own internal knowledge.

Context:
{context}

Conversation History:
{history}

Question: {question}

Answer:"""

prompt = ChatPromptTemplate.from_template(template)

def format_docs(docs):
    """Formats retrieved document chunks into a single block of text."""
    return "\n\n".join(doc.page_content for doc in docs)

def stream_response(message, history):
    """Processes the user message and streams the Gemini response."""
    
    # Create the retriever
    retriever = vector_store.as_retriever(search_kwargs={'k': 5})
    
    # Modern LCEL Chain
    rag_chain = (
        {
            "context": retriever | format_docs, 
            "question": RunnablePassthrough(), 
            "history": lambda x: history
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    # Stream the output
    partial_message = ""
    for chunk in rag_chain.stream(message):
        partial_message += chunk
        yield partial_message

# 5. Gradio Interface
chatbot = gr.ChatInterface(
    fn=stream_response, 
    textbox=gr.Textbox(
        placeholder="Ask a question about your documents...", 
        container=False, 
        scale=7
    ),
    title="Gemini 2.5 RAG Chatbot",
    description="I answer based strictly on the PDFs in your data folder."
)

if __name__ == "__main__":
    # Launch with the theme applied here
    chatbot.launch(theme="soft")