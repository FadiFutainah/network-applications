from rest_framework import serializers

from files.models import File, Log


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'name', 'file']


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ['user', 'operation', 'timestamp', 'file']
