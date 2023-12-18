from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from files.models import File, Log


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'name', 'file']

    def validate(self, attrs):
        if attrs.get('file') is None:
            raise ValidationError()
        return attrs


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ['user', 'operation', 'timestamp', 'file']
