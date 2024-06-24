import requests
import json
import os

def get_repo_contents(owner, repo, target_dir="repo_contents"):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse JSON response
        contents = response.json()
        
        # Create target directory if it does not exist
        os.makedirs(target_dir, exist_ok=True)
        
        # Iterate through contents
        for content in contents:
            if 'download_url' in content:
                # Get file contents
                file_content_response = requests.get(content['download_url'], headers=headers)
                file_content_response.raise_for_status()
                
                # Write file content to local file
                file_path = os.path.join(target_dir, content['name'])
                with open(file_path, 'wb') as f:
                    f.write(file_content_response.content)
                
                print(f"Downloaded: {content['name']}")

            else:
                print(f"Skipping directory: {content['name']}")

        print(f"All files downloaded to {target_dir}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching repository contents: {e}")

# Example usage for the GitGenius repository:
owner = "fuadh246"
repo = "GitGenius"
get_repo_contents(owner, repo)

