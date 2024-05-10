from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

## for langsmith tracking
os.environ["LANGCHAIN_TRACKING_V2"] ="true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You ar a helpful assistant. Please respond to the user querries"),
        ("user","Qusetion:{question}")
    ]
)
## streamlit framework
st.title("Langchain Demo with OPENAI API")
input_text = st.text_input("Search the topic you want")

## OpenAI LLm
llm = ChatOpenAI(model="gpt-3.5-turbo")
output_parser = StrOutputParser()
chain = prompt | llm| output_parser

if input_text:
    st.write(chain.invoke({'question':input_text}))