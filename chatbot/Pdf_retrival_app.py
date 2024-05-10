import io
import os
import tempfile
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
import streamlit as st

# Set title of the Streamlit app
st.title("Chatbot using Llama2 🦙🚀")

# File uploader for PDFs
uploaded_file = st.file_uploader("Choose a PDF file.")

# Text input for questions
question = st.text_input("Ask Qestion Here!")

# Initialize Ollama model and output parser
llm = Ollama(model="llama2")
parser = StrOutputParser()

# If a file is uploaded
if uploaded_file is not None:
    # Save the content of the uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    # Load PDF using PyPDFLoader
    loader = PyPDFLoader(temp_file_path)
    pages = loader.load_and_split()

    # Define template for prompting
    template = """ 
    You are an expert reume analyzer and its your job to give answer to the question based on the context(CV) provided below.
    if you can't answer the question, just say "I don't know".

    Context: {context}

    Question: {question}
    """
    
    # Create a prompt from the template
    prompt = PromptTemplate.from_template(template)

    # Chain the prompt, model, and parser
    chain = prompt | llm | parser

    # Invoke the chain with context and question
    response = chain.invoke({"context": pages, "question": question})

    # Display the response
    st.write(response)

    # Delete the temporary file
    os.unlink(temp_file_path)
