import json
import requests
import secrets
import os
from dotenv import load_dotenv
import re

load_dotenv()

greptileApiKey = os.environ.get("GREPTILE_API_KEY")
githubToken =    os.environ.get("GITHUB_TOKEN")

BASE_URL = 'https://api.greptile.com/v2'

headers = {
    'Authorization': f'Bearer {greptileApiKey}',
    'X-Github-Token': githubToken,
    'Content-Type': 'application/json'
}


SYSTEM_PROMPT = """
    Given specifications are made for student. 
    You have to check if student has done the task so that it meets specifications.
    Check ifs the repository files satisfies given specifications. 
    If all spacifications are satisfied, then send response: 'OK', if not say what is wrong. 
    If the none of the specifications are satisfied , then send response: 'NO'
    """

def make_token(length=32):
    # Creates a cryptographically-secure, URL-safe string
    return secrets.token_urlsafe(length)


def index_repos(owner, repo, branch):
    url = f'{BASE_URL}/repositories'
    payload = {
        "remote": "github",
        "repository": f"{owner}/{repo}",
        "branch": branch
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.json())


def check_indexing_progress(owner, repo, branch):
    repositoryIdentifier = f"github%3A{branch}%3A{owner}%2F{repo}"

    url = f'{BASE_URL}/repositories/{repositoryIdentifier}'

    response = requests.get(url, headers=headers)
    print(response.json())
    return response.json()


def query(system, specs, owner, repo, branch):
    url = f'{BASE_URL}/query'

    sessionId = make_token()
    # sessionId = "pJ1bn3l2Vvo7YpJwT8oYZ3Tk1TnQ7ha8MtZkLg0ltYs" 
    # print()
    # print(sessionId)
    # print()

    payload = {
        "messages": [
            {
                "id": "id-1",
                "content": f"{system}",
                "role": "system"
            },
            {
                "id": "id-2",
                "content": f"Specifications {specs}",
                "role": "user"
            }
        ],
        "repositories": [
            {
                "remote": "github",
                "repository": f"{owner}/{repo}",
                "branch": branch
            }
        ],
        "sessionId": sessionId
    }

    response = requests.post(url, json=payload, headers=headers)
    # print(response.json()["message"]) 

    res = json.loads(response.json()["message"][7:-3])

    code_blocks = []
    for obj in res:
        print(obj["code"])
        code_block = "".join(obj["code"])
        code_blocks.append(code_block)
        print(code_block)
        
    return code_blocks


def search(search_query, owner, repo, branch):
    url = f"{BASE_URL}/search"

    payload = {
        "query": search_query,
        "repositories": [
            {
                "remote": "github",
                "branch": branch,
                "repository": f"{owner}/{repo}"
            }
        ],
        "sessionId": "<string>",
        "stream": True
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    return response.json()



if __name__ == '__main__':
    specification = """
        ### **Level 1:**
        - Creating a basic web layout

        ### **Level 2**:
        - Developing a movie catalog page allowing users to explore various movies, with information about genre, actors, etc.
        - Implementation of search function allows users to search for a movie

        ### **Level 3**:
        - Use the API to get information about the movies
    """

    # branch = "master"
    branch = "main"
    project = {
        "owner": "anuza22",
        "repo": "nFactorial-Project",
        "branch": branch
    }

    # index_repos(**project)
    # check_indexing_progress(**project)
    search_query = """
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
        Do not add any extra characters.
        Give the result in JSON format. 
        ```
    """

    query(search_query, specification, **project)


    # search(search_query, **project)
