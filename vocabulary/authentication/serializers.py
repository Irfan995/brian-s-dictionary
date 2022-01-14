from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        depth = 1

    def create(self, validated_data):
        email = validated_data['email']
        if not User.objects.filter(email=email).exists():
            if validate_password(validated_data['password']) == None:
                password = make_password(validated_data['password'])
                user = User.objects.create(
                    username=validated_data['username'],
                    email=validated_data['email'],
                    password=password
                )
        
            return user
        else:
            raise ValidationError(
                {'email_exists': 'A user with that email already exists.'}
            )
