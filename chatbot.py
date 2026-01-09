import os
import gradio as gr
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

# Configuration
CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "example_collection"

# 1. Initialize Gemini Embeddings
embeddings_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# 2. Connect to Chroma
vector_store = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings_model,
    persist_directory=CHROMA_PATH,
)

# 3. Initialize Gemini 2.5 Flash
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

# 4. Prompt Template
template = """
You are "FarmerBot", a wise and helpful agricultural assistant. 
Use the following context from the Farmer's Handbook to answer the user.

- If the user says 'hello' or 'hi', greet them like a friendly neighbor.
- If you don't know the answer based on the context, offer general farming best practices.
- Keep your answers practical and easy for a farmer to understand.

Context:
{context}

History:
{history}

Question: {question}

Answer:"""

prompt = ChatPromptTemplate.from_template(template)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def stream_response(message, history):
    retriever = vector_store.as_retriever(search_kwargs={'k': 5})
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

    partial_message = ""
    for chunk in rag_chain.stream(message):
        partial_message += chunk
        yield partial_message

def save_chat(history):
    """Saves the current chat history to a text file."""
    chat_text = "--- FarmerBot Chat Log ---\n\n"
    for user_msg, bot_msg in history:
        chat_text += f"Farmer: {user_msg}\nFarmerBot: {bot_msg}\n\n"
    
    file_path = "latest_chat_log.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(chat_text)
    return file_path

# 5. UI Design
with gr.Blocks(title="FarmerBot AI") as demo:
    gr.Markdown("# 🌱 **FarmerBot: Your Agricultural Assistant**")
    
    with gr.Row():
        chat_interface = gr.ChatInterface(
            fn=stream_response,
            examples=["What are the steps for soil testing?", "How to manage weeds?", "Importance of seed treatment?"],
        )

    with gr.Row():
        download_btn = gr.Button("💾 Save Chat History to File")
        file_output = gr.File(label="Download Chat Log")

    # Link the save button to the function
    # Note: chat_interface.chatbot is the component that holds the history
    download_btn.click(fn=save_chat, inputs=[chat_interface.chatbot], outputs=file_output)

if __name__ == "__main__":
    # Cleanest launch possible for maximum compatibility
    demo.launch()