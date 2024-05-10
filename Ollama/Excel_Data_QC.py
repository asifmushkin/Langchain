from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
#from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_community.document_loaders import unstructured

import streamlit as st


st.title("QC application with llama3!")
loader = unstructured("D:\Pavement\Excel Workbook\Distress_Workbook\E_Keycode.xlsx", mode="elements")
docs = loader.load()

llm = Ollama(model = "Llama3")
template = (
    """You ar a helpful assistant. your job is to find typo errors in the column of COMMENT_1 of given
         below data. Please respond to the user querries. if you don't know say i don't know.
         data:{data}"""
    
)
prompt = PromptTemplate.from_template(template)

out_parser = StrOutputParser

chain = prompt|llm|out_parser

text_input = st.text_input("Ask any question")

if text_input:
    pass