from django.urls import path, include
from github.views import check

from github.views import check_cheating, check_requirements

urlpatterns = [
    path('/', check),
    path('check_cheating', check_cheating),
    path('check_requirements', check_requirements),
]