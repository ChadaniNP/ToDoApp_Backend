from django.urls import path
from todoapp.views import RegisterView, LoginView, LogoutView, TodoCreateView

urlpatterns =[
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'), #path('logout/', LogoutView.as_view(), name='logout')
    path('todos/', TodoCreateView.as_view(), name='todo-create'),

]