from rest_framework import serializers

from core.models import Module

class ModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Module
        fields = ('id', 'name')
        read_only_fields = ('id', )