import os
import shutil
import git
import tiktoken
from langchain_openai import OpenAIEmbeddings
import time

def clone_repo(repo_url, clone_dir):
    """
    Clones a GitHub repository into a specified directory.
    If the directory already exists, it deletes the directory first.
    """
    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir)  # Remove the existing directory

    # Clone the repository into the specified directory
    git.Repo.clone_from(repo_url, clone_dir)

    return clone_dir

def read_files_from_repo(clone_dir):
    """
    Reads all files from the cloned repository.
    Returns a dictionary where keys are file paths and values are file contents.
    """
    repo_contents = {}

    for root, dirs, files in os.walk(clone_dir):
        if '.git' in dirs:
            dirs.remove('.git')  # Remove the .git directory
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    repo_contents[file_path] = f.read()
            except UnicodeDecodeError:
                try:
                    with open(file_path, 'r', encoding='latin-1') as f:
                        repo_contents[file_path] = f.read()
                except UnicodeDecodeError:
                    print(f"Skipping file due to encoding error: {file_path}")

    return repo_contents

# def num_tokens_from_string(string: str, encoding_name: str) -> int:
#     """
#     Returns the number of tokens in a text string using a specified encoding.
#     """
#     encoding = tiktoken.get_encoding(encoding_name)
#     num_tokens = len(encoding.encode(string))
#     return num_tokens

# def embed_texts(openai_api_key, preprocessed_contents, batch_size=1000, delay=10):
#     """
#     Embeds text content using OpenAIEmbeddings.
#     Returns a dictionary where keys are file names and values are embeddings.
#     """
#     embedded_contents = {}
#     embeddings_instance = OpenAIEmbeddings(api_key=openai_api_key)  # Updated constructor

#     total_tokens = 0
#     batch_contents = []

#     for filename, content in preprocessed_contents.items():
#         tokens = num_tokens_from_string(content, 'gpt2')
#         total_tokens += tokens

#         if total_tokens > batch_size:
#             # Embed the current batch and reset
#             batch_texts = [text for _, text in batch_contents]
#             embedding = embeddings_instance.embed_documents(batch_texts)
#             for i, (fname, _) in enumerate(batch_contents):
#                 embedded_contents[fname] = embedding[i]
#                 print(f"Embedded {fname}")

#             # Clear the batch and reset the token count
#             batch_contents = []
#             total_tokens = tokens

#             # Add a delay to respect the rate limit
#             time.sleep(delay)

#         # Add the current file to the batch
#         batch_contents.append((filename, content))

#     # Embed any remaining contents in the last batch
#     if batch_contents:
#         batch_texts = [text for _, text in batch_contents]
#         embedding = embeddings_instance.embed_documents(batch_texts)
#         for i, (fname, _) in enumerate(batch_contents):
#             embedded_contents[fname] = embedding[i]
#             print(f"Embedded {fname}")

#     return embedded_contents