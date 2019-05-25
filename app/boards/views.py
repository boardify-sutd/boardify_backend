from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
from core.models import Module
from boards import serializers

class ModuleViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage Modules in the database"""

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = Module.objects.all()
    serializer_class = serializers.ModuleSerializer