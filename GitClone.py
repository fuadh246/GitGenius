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