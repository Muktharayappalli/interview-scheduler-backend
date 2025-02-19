from django.urls import path
from . import views

urlpatterns = [
    path('register/availability/', views.register_availability),
    path('get/interview_slots/', views.get_interview_slots),
]