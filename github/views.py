from django.http import JsonResponse
import json
import github.handlers as handlers

import github.greptile as greptile
from django.views.decorators.csrf import csrf_exempt


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
        
        result = handlers.check_cheating(task_criteria, owner, repo, branch)
        return JsonResponse({'results': result})
        

    else:
        return JsonResponse({'error': 'Invalid method'}, status=400)



def check_requirements(request):
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
        
        result = greptile.check_requirments(task_criteria, owner, repo, branch)
        return JsonResponse({'results': result})
        

    else:
        return JsonResponse({'error': 'Invalid method'}, status=400)