from django.urls import path, include
from github.views import check


urlpatterns = [
    path('/', check)
]