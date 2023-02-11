"""
views for user api
"""
from rest_framework import generics
from user import serializers

class CreateUserView(generics.CreateAPIView): #create api view handles post requests for creating objects in the db
    """"Create a new user in the system"""
    serializer_class = serializers.UserSerializer
