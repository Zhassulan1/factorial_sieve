import json
import os
import github.greptile as greptile
import requests
import zipfile
import os
import github.greptile as greptile
import github.gh_search as gh_search
import random


FIND_KEY_POINTS = """
        Find code blocks related to key points of tasks realization. 
        Find only key points of code. 
        And this key points should be related to given task criteria.
        If there is many code blocks are related to one key point,
        and are placed next to each other,
        then, you should join them into one code block.
        Give citations in the following format:

        ```json
        [
            {
                "purpose": "purpose of code block",
                "code": "code block"
            },
            {
                "purpose": "purpose of code block",
                "code": "code block"
            },
            .....    
        ]
        Do not add any other fields. 
        You should only give code citations from codebase. 
        Examples should be only from current repository. Do not add any code.
        Do not add any extra characters.
        Give the result in JSON format. 
        ```
    """


specification = """
        ### **Level 1:**
        - Creating a basic web layout

        ### **Level 2**:
        - Developing a movie catalog page allowing users to explore various movies, with information about genre, actors, etc.
        - Implementation of search function allows users to search for a movie

        ### **Level 3**:
        - Use the API to get information about the movies
    """


def create_zip(name, text):
    PROJ_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Divide the text into two parts
    mid_index = len(text) // 2
    part1 = text[:mid_index]
    part2 = text[mid_index:]
    
    # Create the temporary file paths
    tmp_file_path1 = os.path.join(PROJ_DIR, "_tmp_file_1.ts")
    tmp_file_path2 = os.path.join(PROJ_DIR, "_tmp_file_2.ts")
    
    # Write each part to a separate temporary file
    with open(tmp_file_path1, "w+", encoding='utf-8') as f1:
        f1.write(part1)
    with open(tmp_file_path2, "w+", encoding='utf-8') as f2:
        f2.write(part2)
    
    # Create the ZIP file
    zip_file_path = os.path.join(PROJ_DIR, f"{name}.zip")
    with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(tmp_file_path1, "file1.ts")
        zf.write(tmp_file_path2, "file2.ts")
    
    # Remove the temporary files
    os.remove(tmp_file_path1)
    os.remove(tmp_file_path2)
    return zip_file_path


def check_index(owner, repo, branch):
    index = greptile.index_repos(owner, repo, branch)
    status = greptile.check_indexing_progress(owner, repo, branch)
    index_status = status.get("status")
    if index_status == 'completed':
        return True
    return False


def submit_to_dolos(name, zipfile_path):
   """
   Submit a ZIP-file to the Dolos API for plagiarism detection
   and return the URL where the resulting HTML report can be found.
   """
   response = requests.post(
      'https://dolos.ugent.be/api/reports',
      files = { 'dataset[zipfile]': open(zipfile_path, 'rb') },
      data = { 'dataset[name]': name }
   )
   res = response.json()

   return res["html_url"]


def check_cheating(specs, owner, repo, branch):
    key_points = greptile.query(specs, owner, repo, branch)
    print(key_points)
    text = " ".join(key_points)

    zip_file_path = create_zip(owner, text)
    result = submit_to_dolos(owner, zip_file_path)
    print(result)
    return result


if __name__ == "__main__":
    branch = "main"
    project = {
        "owner": "anuza22",
        "repo": "nFactorial-Project",
        "branch": branch,
    }
    check_cheating(FIND_KEY_POINTS, specification, **project)