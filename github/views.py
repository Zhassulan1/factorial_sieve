from django.http import JsonResponse
from django.shortcuts import render


# Create your views here.
def check(request):
    return JsonResponse({'results': "res"})