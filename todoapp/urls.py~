from django.urls import path
from todoapp.views import RegisterView, LoginView, LogoutView, TodoCreateView, TodoUpdateView, TodoListView

urlpatterns =[
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'), #path('logout/', LogoutView.as_view(), name='logout')
    path('todos/', TodoListView.as_view(), name='todo-list'),
    path('todos/', TodoCreateView.as_view(), name='todo-create'),
    path('todos/<int:pk>/', TodoUpdateView.as_view(), name='todo-update'),
    # path('todos/<int:pk>/delete/', TodoDeleteView.as_view(), name='todo-delete'),  # Delete a todo

]