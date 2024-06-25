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

from gitgenius import clone_repo, read_files_from_repo, embed_texts




if __name__ == "__main__":
    repo_url = 'https://github.com/fuadh246/GitGenius'  # Replace with your GitHub repository URL
    clone_dir = os.path.join(os.getcwd(), 'cloned_repo')  # Define the path for the cloned repository
    clone_dir = clone_repo(repo_url, clone_dir)
    preprocessed_contents = read_files_from_repo(clone_dir)
    openai_api_key = os.environ.get("OPENAI_API_KEY")  # Ensure you have your API key set
    print(f"Total files: {len(preprocessed_contents)}")
    embedded_contents = embed_texts(openai_api_key, preprocessed_contents)
    
