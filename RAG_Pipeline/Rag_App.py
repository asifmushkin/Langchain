from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
import streamlit as st
import os

embeddings = OllamaEmbeddings()
model_llm = ChatOllama(model="llama2")
output_parser = StrOutputParser()

# Initialize Streamlit app
st.title("Chatbot using RAG and Llama2")

# Create the "temp" directory if it doesn't exist
if not os.path.exists("temp"):
    os.makedirs("temp")

# Display file uploader
uploaded_file = st.file_uploader("Upload a file:", type=None)
absolute_path = None

if uploaded_file is not None:
    # Save the uploaded file to the "temp" directory
    with open(os.path.join("temp", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getvalue())
    absolute_path = os.path.abspath(os.path.join("temp", uploaded_file.name))

# Text input for user's question
question = st.text_input("Ask your question here!")
if question is not None and absolute_path is not None:  # Check if a file has been uploaded
    loader = PyPDFLoader(absolute_path).load()
    text_spliter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    text_chunk = text_spliter.split_documents(documents=loader)
    vector_store = FAISS.from_documents(text_chunk, embeddings)
    retriever = vector_store.as_retriever()

    template = """You are the assistant to the Questions and Answering tasks. Use the following pieces of retrieved context
                to answer the question. If you don't know the answer, just say that you don't know. Use four sentences maximum and keep the
                answer concise.
                Question:{question}
                Context:{context}
                Answer:
                """
    prompt = ChatPromptTemplate.from_template(template=template)
    rag_chain = ({"context": retriever, "question": RunnablePassthrough()} | prompt | model_llm | output_parser)
    response = rag_chain.invoke(question)
    
    st.write(response)
