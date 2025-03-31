from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Todo

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': False}}  # Ensure password is not exposed

    def create(self, validated_data):
        raw_password = validated_data['password']  # Get raw password
        print(f"🔍 Debug: Raw password before hashing: {raw_password}")

        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(raw_password)  # Hash the password
        user.save()

        print(f"✅ Debug: Hashed password stored: {user.password}")  # Should start with pbkdf2_sha256$
        return user


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'title', 'description', 'completed', 'created_at']
