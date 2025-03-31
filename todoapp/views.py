from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from todoapp.serializers import UserSerializer
from .models import Todo
from .serializers import TodoSerializer
from rest_framework.permissions import AllowAny

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(LoginView, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user_id})

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=200)

# Create Todo View
class TodoCreateView(generics.CreateAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can create todos

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Save the todo with the logged-in user

class TodoListView(generics.ListAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Override the default queryset to return only the todos for the authenticated user.
        """
        return Todo.objects.filter(user=self.request.user)

# Update Todo View
class TodoUpdateView(generics.UpdateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]  # Requires authentication

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

#     # Delete Todo
#
# class TodoDeleteView(generics.DestroyAPIView):
#     serializer_class = TodoSerializer
#     permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
#
#     def get_queryset(self):
#         """
#         Override the default queryset to ensure that only todos belonging
#         to the authenticated user can be deleted.
#         """
#         return Todo.objects.filter(user=self.request.user)