# tests/test_models.py
import pytest
from todoapp.models import Todo

@pytest.mark.django_db
def test_todo_model():
    todo = Todo.objects.create(title="Test Todo", description="This is a test")
    assert todo.title == "Test Todo"
    assert todo.description == "This is a test"
