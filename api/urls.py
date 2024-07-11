from django.urls import path
from . import views

urlpatterns = [
    path('evaluate-applicants/', views.evaluate_applicants),
]