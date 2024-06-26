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
from langchain.schema.document import Document
from GitClone import clone_repo, read_files_from_repo

import warnings
warnings.filterwarnings("ignore")




if __name__ == "__main__":
    repo_url = 'https://github.com/fuadh246/GitGenius'  # Replace with your GitHub repository URL
    clone_dir = os.path.join(os.getcwd(), 'cloned_repo')  # Define the path for the cloned repository
    clone_dir = clone_repo(repo_url, clone_dir)
    preprocessed_contents = read_files_from_repo(clone_dir)
    openai_api_key = os.environ.get("OPENAI_API_KEY")  # Ensure you have your API key set
    
    embeddings_instance = OpenAIEmbeddings(api_key=openai_api_key)
    
    texts= list(zip(preprocessed_contents.keys(), preprocessed_contents.values())) #testing
    documents = [Document(page_content=text[1], metadata={'page_name': text[0], 'source': text[0]}) for text in texts]

    
    db = FAISS.from_documents(documents= documents, embedding=embeddings_instance)
    db.save_local(os.path.join(os.getcwd(), "vector_database/"))
    
    vectorStore = FAISS.load_local("vector_database", embeddings_instance, allow_dangerous_deserialization=True)
    
    retriever = vectorStore.as_retriever(search_type="similarity", search_kwargs={'k':5})
    
    
    query = "how do I clone a git repo?"
    
    docs = retriever.get_relevant_documents(query)
    docs_content = "\n".join([doc.page_content for doc in docs])
    prompt = f'''You are given project code files. Given the query specified here: {query}, analyze the code files and output the response.

    {docs_content}'''

    llm = ChatOpenAI()
    
    chain = load_qa_with_sources_chain(llm=llm, chain_type="stuff")
    
    result = chain.run(input_documents=docs, question=query)
    
    print(result)