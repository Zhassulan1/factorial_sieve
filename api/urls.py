from django.urls import path
from . import views

urlpatterns = [
    path('evaluate-applicants/', views.evaluate_applicants),
    path('notify_all_applicants/', views.notify_all_applicants),
]