import os
import greptile as greptile
import gh_search as gh_search
import random

# FIND_KEY_POINTS = """
#         Find code blocks related to key points of tasks realization. 
#         Find only key points of code. 
#         And this key points should be related to given task criteria.
#         If there is many code blocks are related to one key point,
#         and are placed next to each other,
#         then, you should join them into one code block.
#         Give citations in the following format:

#         ```json
#         [
#             {
#                 'purpose': 'purpose of code block',
#                 'code': 'code block'
#             },
#             {
#                 'purpose': 'purpose of code block',
#                 'code': 'code block'
#             },
#             .....    
#         ]
#         Do not add any other fields. 
#         You should only give code citations from codebase. 
#         Do not add any extra characters.
#         Give the result in JSON format. 
#         ```
#     """



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

# def search_by_chunks(search_query, chunk_size=100):
#     current = 0
#     if len(search_query) < 150:
#         chunk = search_query
#         res = gh_search.code_search(chunk)
#         print(res)
#         print("\n"*5)
#         return


#     while current < len(search_query):
#         x = random.randint(5, 20)
#         if current + chunk_size + x < len(search_query):
#             chunk = search_query[current:current+chunk_size].replace("\n", "+").replace(" ", "+")
#             print(chunk)
#             current += chunk_size + x

#             res = gh_search.code_search(chunk)
#             print(res)
#             print("\n"*5)
#         break


# def check_cheating(system, specs, owner, repo, branch):
#     key_points = greptile.query(system, specs, owner, repo, branch)

#     for i, point in enumerate(key_points):
#         search_by_chunks(point)
#         print(f"Point {i} checked: ")


def check_cheating(system, specs, owner, repo, branch):
    key_points = greptile.query(system, specs, owner, repo, branch)
    for i, point in enumerate(key_points):
        greptile.search(point, )
        print(f"Point {i} checked: ")
        print(point)
        print("\n"*5)

if __name__ == "__main__":
    # branch = "master"
    branch = "main"
    project = {
        "owner": "anuza22",
        "repo": "nFactorial-Project",
        "branch": branch,
    }
    check_cheating(FIND_KEY_POINTS, specification, **project)