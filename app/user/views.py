from django.shortcuts import render

# Create your views here.
from .serializers import UserSerializer
from rest_framework import generics

class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer

    


