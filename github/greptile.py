import json
import requests
import secrets
import os
from dotenv import load_dotenv
import re

load_dotenv()

GREPTILE_API_KEY = os.environ.get("GREPTILE_API_KEY")
GITHUB_TOKEN =    os.environ.get("GITHUB_TOKEN")

BASE_URL = 'https://api.greptile.com/v2'

HEADERS = {
    'Authorization': f'Bearer {GREPTILE_API_KEY}',
    'X-Github-Token': GITHUB_TOKEN,
    'Content-Type': 'application/json'
}

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
        ```
        Do not add any other fields. 
        You should only give code citations from codebase. 
        Examples should be only from current repository. Do not add any code.
        Do not add any extra characters.
        Give the result in JSON format. 
    """

CHECK_REQUIREMENTS_SYSTEM_PROMPT = """
    Given specifications are made for student. 
    You have to check if student has done the task so that it satisfies requirements.
    Check ifs the repository files satisfies given requirements.
    Response must have following format:
    {
        "verdict": "OK|NO|ARGUABLE",
        "summary": "summary of the verdict"
    }

    "verdict" can be only/ one of the following:
    OK - student has done the task so that it satisfies ALL OF THE requirements.
    NO - student has not done the task so that it satisfies requirements, or it does not satisfy enough.
    ARGUABLE - student has done the task so that it satisfies some of the requirements, but not all.
    
    "summary" must explain reasoning of verdict. It should be short and clear.
    """




def make_token(length=32):
    return secrets.token_urlsafe(length)


def index_repos(owner, repo, branch):
    url = f'{BASE_URL}/repositories'
    payload = {
        "remote": "github",
        "repository": f"{owner}/{repo}",
        "branch": branch
    }
    print(payload)
    response = requests.post(url, json=payload, headers=HEADERS)
    print(response.json())


def check_indexing_progress(owner, repo, branch):
    repositoryIdentifier = f"github%3A{branch}%3A{owner}%2F{repo}"

    url = f'{BASE_URL}/repositories/{repositoryIdentifier}'

    response = requests.get(url, headers=HEADERS)
    return response.json()


def query(specs, owner, repo, branch):
    url = f'{BASE_URL}/query'
    sessionId = make_token()

    payload = {
        "messages": [
            {
                "id": "id-1",
                "content": FIND_KEY_POINTS,
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

    response = requests.post(url, json=payload, headers=HEADERS)
    res = json.loads(response.json()["message"][7:-3])

    code_blocks = []
    for obj in res:
        print(obj["code"])
        code_block = "".join(obj["code"])
        code_blocks.append(code_block)
        print(code_block)

    return code_blocks


def check_requirments(specs, owner, repo, branch):
    url = f'{BASE_URL}/query'
    sessionId = make_token()
    payload = {
        "messages": [
            {
                "id": "id-1",
                "content": CHECK_REQUIREMENTS_SYSTEM_PROMPT,
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

    response = requests.post(url, json=payload, headers=HEADERS)

    res = json.loads(response.json()["message"][7:-3])
    return res







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





# def search(search_query, own_repo, branch, repo_list):
#     url = f"{BASE_URL}/search"

#     query = """
#         Find any code that is same as given below code.
#     """


#     repositories = []

#     for repo in repo_list:
#         if repo[19:] != own_repo[19:]:    
#             repositories.append({
#                 "remote": "github",
#                 "branch": branch,
#                 "repository": repo[19:]
#             })

#     payload = {
#         "query": query + search_query,
#         "repositories": repositories,
#         "sessionId": "<string>",
#         "stream": True
#     }

#     response = requests.request("POST", url, json=payload, headers=HEADERS)

#     return response.json()