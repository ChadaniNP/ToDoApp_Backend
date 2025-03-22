from django.urls import path

from todoapp.views import RegisterView

urlpatterns =[
    path('register/', RegisterView.as_view(), name='register'),
]