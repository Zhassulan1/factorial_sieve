from django.urls import path, include
from github.views import check

from github.views import check_cheating

urlpatterns = [
    path('/', check),
    path('check_cheating', check_cheating),
]