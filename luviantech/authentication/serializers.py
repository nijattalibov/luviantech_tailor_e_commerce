from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser

class UserRegisterSerializer(ModelSerializer):
        class Meta:
            model=CustomUser
            fields=[
                'email',
                'username',
                'password',
                ]

        def validate(self,attr):
           # validate password
           validate_password(attr['password'])
           return attr
       
        