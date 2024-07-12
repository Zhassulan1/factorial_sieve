from django.http import JsonResponse
import json
import github.handlers as handlers

import github.greptile as greptile
from django.views.decorators.csrf import csrf_exempt


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

def check(request):
    return JsonResponse({'results': "res"})

@csrf_exempt
def check_cheating(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f"Parsed JSON data: {data}")
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        try:
            repo = data.get('repository')
            print(f"repository: {repo}")

            owner = data.get('owner')
            print(f"owner: {owner}")

            branch = data.get('branch')
            print(f"branch: {branch}")

            task_criteria = data.get('task_criteria')
            print(f"task_criteria: {task_criteria}")

        except Exception as e:
            print(e)
            return JsonResponse({'error': 'Unexpected Fields'}, status=400)
        
        is_indexed = handlers.check_index(owner, repo, branch)
        if not is_indexed:
            return JsonResponse({'Indexing': 'Repository is currently being indexed, it will '}, status=200)
        
        result = handlers.check_cheating(FIND_KEY_POINTS, task_criteria, owner, repo, branch)
        return JsonResponse({'results': result})
        

    else:
        return JsonResponse({'error': 'Invalid method'}, status=400)
