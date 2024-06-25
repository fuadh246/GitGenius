import openai
import os
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.qa_with_sources.loading import load_qa_with_sources_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI



openai.api_key = os.environ.get("OPENAI_API_KEY")    #input your api key here

prompt= f'''You are given project code files.

Given the query specified here: {query},

Analyze the code files and output the response
'''


query=""

embeddings = OpenAIEmbeddings()

db= FAISS(embeddings, docstore) #input vector database credentials here

retriever = db.as_retriever(search_kwargs={'k': 4})

docs= retriever.get_relevant_documents(query)

llm= ChatOpenAI()


chain= load_qa_with_sources_chain(llm=llm, chain_type="stuff")