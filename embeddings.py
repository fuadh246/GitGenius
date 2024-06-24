import tiktoken 
import os
from langchain.embeddings import OpenAIEmbeddings  # Uncomment this import


openai_api_key = os.environ.get("OPENAI_API_KEY")
if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable is not set")
print("OpenAI API key is set")
print("Embedding contents...")
print("This may take a while...")
print("========================================")
def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def preprocess_text(text):
    text = text.replace('\n', ' ').replace('\r', ' ')
    preprocessed_contents = {file: preprocess_text(content) for file, content in repo_contents.items()}
    return text

def embed_texts(openai_api_key, preprocessed_contents):
    embedded_contents = {}
    # Initialize OpenAIEmbeddings
    embeddings_instance = OpenAIEmbeddings(openai_api_key=openai_api_key)
    
    for filename, content in preprocessed_contents.items():
        embedding = embeddings_instance.embed(content)
        embedded_contents[filename] = embedding
    return embedded_contents