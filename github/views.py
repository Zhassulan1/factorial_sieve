from django.http import JsonResponse
import json

import github.greptile
import github.gh_search as gh_search


# SYSTEM_PROMPT_FOR_TASK_REALTED_CODE = """
#     User prompt below gives you the task criteria and specifications.
#     You should return 
# """

def check(request):
    return JsonResponse({'results': "res"})


def check_cheating(request):
    if request.method == 'POST' :
        try:
            data = json.loads(request.body)
            print(f"Parsed JSON data: {data}")
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        try:
            repo = data.get('repository')
            print(f"repository: {repo}")

            owner = repo.get('owner')
            print(f"owner: {owner}")

            branch = repo.get('branch')
            print(f"branch: {branch}")

            task_criteria = repo.get('task_criteria')
            print(f"task_criteria: {task_criteria}")

        except Exception as e:
            print(e)
            return JsonResponse({'error': 'Unexpected Fields'}, status=400)

        

    else:
        return JsonResponse({'error': 'Invalid method'}, status=400)
