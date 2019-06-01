from rest_framework import serializers

from core.models import *

class ModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Module
        fields = ('id', 'name')
        read_only_fields = ('id', )


"""Location, Lessons, Lecturers, Boards"""

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ('code', 'name')

class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = ('type', 'over', 'module', 'location', "lesson_time")


class LecturerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lecturer
        fields = ('name', 'user', 'lessons')

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('image_url', 'lesson', 'text_on_board', 'time_taken')