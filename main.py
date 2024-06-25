import os
import shutil
import git
import tiktoken
from langchain_openai import OpenAIEmbeddings
import time
import openai
import os
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.qa_with_sources.loading import load_qa_with_sources_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI

from GitClone import clone_repo, read_files_from_repo




if __name__ == "__main__":
    repo_url = 'https://github.com/fuadh246/GitGenius'  # Replace with your GitHub repository URL
    clone_dir = os.path.join(os.getcwd(), 'cloned_repo')  # Define the path for the cloned repository
    clone_dir = clone_repo(repo_url, clone_dir)
    preprocessed_contents = read_files_from_repo(clone_dir)
    openai_api_key = os.environ.get("OPENAI_API_KEY")  # Ensure you have your API key set
    
    embeddings_instance = OpenAIEmbeddings(api_key=openai_api_key)
    
    db = FAISS.from_documents(documents= preprocessed_contents, embedding=embeddings_instance)
    db.save_local(os.path.join(os.getcwd(), "vector_database/"))
    vectorStore = FAISS.load_local("vector_database/", embeddings_instance)
    
    retriever = vectorStore.as_retriever(search_type="similarity", search_kwargs={'k':5})
    
    prompt= f'''You are given project code files. Given the query specified here: {query}, Analyze the code files and output the response.'''
    
    query="how do i clone git repo?"
    
    llm= ChatOpenAI()
    
    chain= load_qa_with_sources_chain(llm=llm, chain_type="stuff")
    
    docs = retriever.get_relevant_documents(query)
    
    result = chain.run(input_documents=docs, question=query)
    
    print(result)
    
