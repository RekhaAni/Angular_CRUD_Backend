from django.urls import path
from .views import StudentAPI

urlpatterns = [
    path('students/', StudentAPI.as_view()),                     
    path('students/create/', StudentAPI.as_view()),              
    path('students/update/<int:id>/', StudentAPI.as_view()),    
    path('students/delete/<int:id>/', StudentAPI.as_view()),     
]