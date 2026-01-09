import os
import gradio as gr
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from ui_config import custom_css, hero_html

load_dotenv()

CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "example_collection"
embeddings_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
vector_store = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings_model,
    persist_directory=CHROMA_PATH,
)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

template = """You are FarmerBot. Answer based on context: {context} \nHistory: {history} \nQuestion: {question}"""
prompt = ChatPromptTemplate.from_template(template)

def chat_func(message, history):
    retriever = vector_store.as_retriever(search_kwargs={'k': 3})
    rag_chain = (
        {"context": retriever | (lambda docs: "\n\n".join(d.page_content for d in docs)), 
         "question": RunnablePassthrough(), "history": lambda x: history}
        | prompt | llm | StrOutputParser()
    )
    response = ""
    for chunk in rag_chain.stream(message):
        response += chunk
        yield response

with gr.Blocks(title="FarmerBot AI Portal") as demo:
    gr.HTML(hero_html)
    with gr.Column(elem_id="floating_container"):
        gr.HTML('<div class="widget-header"><span>🌱</span> FarmerBot AI</div>')
        gr.ChatInterface(fn=chat_func)

if __name__ == "__main__":
    demo.launch(css=custom_css, theme=gr.themes.Soft(primary_hue="emerald"))
