from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Todo


class UserAuthTests(TestCase):
    def setUp(self):
        """Set up user and API client for authentication tests"""
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.client.login(username='testuser', password='testpassword')

    def test_user_registration(self):
        """Test user registration"""
        url = reverse('register')  # Adjust URL name if needed
        data = {
            'username': 'newuser',
            'password': 'newpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_user_login(self):
        """Test login and receiving a token"""
        url = reverse('login')  # Adjust URL name if needed
        data = {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user_id', response.data)

    class UserAuthTests(APITestCase):

        def setUp(self):
            # Create a user for testing
            self.user = User.objects.create_user(username='testuser', password='testpassword')
            self.token = Token.objects.create(user=self.user)  # Generate an authentication token

        def test_user_logout(self):
            # Prepare the logout request with the Authorization header
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)  # Attach token to request

            response = self.client.post('/api/logout/')  # Assuming this is your logout endpoint

            # Assert that the status code returned is 200 OK
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # Optionally, check if the token is deleted (you can query for the token to ensure it's gone)
            with self.assertRaises(Token.DoesNotExist):
                Token.objects.get(key=self.token.key)
    def test_user_login_invalid(self):
        """Test login with invalid credentials"""
        url = reverse('login')
        data = {
            'username': 'invaliduser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# class TodoTests(TestCase):
#     def setUp(self):
#         """Set up user and todo data for CRUD tests"""
#         self.client = APIClient()
#         self.user = User.objects.create_user(username="testuser", password="testpassword")
#         self.client.login(username='testuser', password='testpassword')
#         self.todo_data = {
#             'title': 'Test Todo',
#             'description': 'This is a test todo item.',
#             'completed': False
#         }
#         self.todo = Todo.objects.create(user=self.user, **self.todo_data)
#
#     def test_create_todo(self):
#         """Test creating a todo item"""
#         url = reverse('todo-create')  # Adjust URL name if needed
#         data = {
#             'title': 'New Todo',
#             'description': 'This is a new todo item.',
#             'completed': False
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Todo.objects.count(), 2)
#
#     def test_todo_list(self):
#         """Test retrieving the todo list for the authenticated user"""
#         url = reverse('todo-list')  # Adjust URL name if needed
#         response = self.client.get(url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)  # Only one todo for the user
#
#     def test_todo_update(self):
#         """Test updating an existing todo item"""
#         url = reverse('todo-update', kwargs={'pk': self.todo.id})  # Adjust URL name if needed
#         data = {
#             'title': 'Updated Todo',
#             'description': 'Updated description.',
#             'completed': True
#         }
#         response = self.client.put(url, data, format='json')
#         self.todo.refresh_from_db()
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(self.todo.title, 'Updated Todo')
#         self.assertEqual(self.todo.description, 'Updated description.')
#         self.assertTrue(self.todo.completed)
#
#     def test_todo_delete(self):
#         """Test deleting a todo item"""
#         url = reverse('todo-delete', kwargs={'pk': self.todo.id})  # Adjust URL name if needed
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         with self.assertRaises(Todo.DoesNotExist):
#             Todo.objects.get(id=self.todo.id)
#
#     def test_todo_create_unauthenticated(self):
#         """Test that unauthenticated users cannot create todos"""
#         self.client.logout()
#         url = reverse('todo-create')  # Adjust URL name if needed
#         data = {
#             'title': 'New Todo',
#             'description': 'This is a new todo item.',
#             'completed': False
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#
# class TodoAPITests(TestCase):
#     def setUp(self):
#         """Setup for API client with authentication"""
#         self.client = APIClient()
#         self.user = User.objects.create_user(username="testuser", password="testpassword")
#         self.client.login(username='testuser', password='testpassword')
#
#     def test_todo_api_create(self):
#         """Test creating a Todo item through the API"""
#         url = reverse('todo-list')  # Assuming API list view allows creation via POST
#         data = {
#             'title': 'Test Todo API',
#             'description': 'This is a test todo for API.',
#             'completed': False
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Todo.objects.count(), 1)
#
#     def test_todo_api_list(self):
#         """Test the API to list todos"""
#         url = reverse('todo-list')  # Adjust if needed
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_todo_api_update(self):
#         """Test the API to update a todo"""
#         todo = Todo.objects.create(user=self.user, title="Test Todo", description="Some description")
#         url = reverse('todo-detail', kwargs={'pk': todo.id})  # Adjust URL name if needed
#         data = {
#             'title': 'Updated API Todo',
#             'description': 'Updated description for API.',
#             'completed': True
#         }
#         response = self.client.put(url, data, format='json')
#         todo.refresh_from_db()
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(todo.title, 'Updated API Todo')
#
#     def test_todo_api_delete(self):
#         """Test the API to delete a todo"""
#         todo = Todo.objects.create(user=self.user, title="Test Todo", description="Some description")
#         url = reverse('todo-detail', kwargs={'pk': todo.id})  # Adjust URL name if needed
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         with self.assertRaises(Todo.DoesNotExist):
#             Todo.objects.get(id=todo.id)
