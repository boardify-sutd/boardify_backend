from django.http import HttpResponse
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import render

# Create your views here.
from core.models import *
from boards import serializers

def process_board(request):
    return HttpResponse("process_board")

class ModuleViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    """Manage Modules in the database"""

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = Module.objects.all()
    serializer_class = serializers.ModuleSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by("-name")

    def perform_create(self, serializer):
        """Create a new tag"""
        serializer.save(user=self.request.user)

class LocationViewSet(viewsets.ReadOnlyModelViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):

    """Manage Location in databsase"""
    queryset = Location.objects.all()
    serializer_class = serializers.LocationSerializer

    def get_queryset(self):
        """Return list of locations"""
        return self.queryset


class LessonViewSet(viewsets.ReadOnlyModelViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    queryset = Lesson.objects.all()
    serializer_class = serializers.LessonSerializer

    def get_queryset(self):
        """Return list of lessons"""
        return self.queryset


class LecturerViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    queryset = Lecturer.objects.all()
    serializer_class = serializers.LecturerSerializer
    #
    # def get_queryset(self):
    #     """Return list of lessons"""
    #     return self.queryset


class BoardViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin):

    queryset = Board.objects.all()
    serializer_class = serializers.BoardSerializer






