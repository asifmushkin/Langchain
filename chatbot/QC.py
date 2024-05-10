import io
import os
import tempfile
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_community.document_loaders import csv_loader
import streamlit as st

# Set title of the Streamlit app
st.title("Chatbot using Llama2 🦙🚀")

# File uploader for PDFs
uploaded_file = st.file_uploader("Choose a excel file.")

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
    loader = csv_loader("D:\_2.Programming\_2.VisualCode\Langchain_updated\chatbot\QC.csv")
    pages = loader.load()

    # Define template for prompting
    template = """ 
    you are an expert in MS.Excel and data science. It is your job to find typo errors in the column name comment_1 of given data.
    give response to questions
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
