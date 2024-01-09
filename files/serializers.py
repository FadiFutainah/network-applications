from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from files.models import File, FilesGroup


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'file', 'editor', 'name']
        extra_kwargs = {
            'editor': { 'read_only': True },
        }

    name = serializers.SerializerMethodField()

    def get_name(self, instance):
        return instance.file.name

    def validate(self, attrs):
        if attrs.get('file') is None:
            raise ValidationError('file cant be null or blank.')
        return attrs
    
    def create(self, validated_data):
        file = super().create(validated_data)
        user = self.context['request'].user
        user_group, _ = FilesGroup.objects.get_or_create(owner=user, name=f'{user.username} group')
        user_group.users.add(user)
        user_group.files.add(file)
        return file

class CheckInSerializer(serializers.Serializer):
    files_ids = serializers.ListField()

    def validate(self, attrs):
        files_ids = attrs['files_ids']
        self.file_list = File.objects.filter(id__in=files_ids)
        for file in self.file_list:
            if file.editor is not None:
                raise ValidationError(f'file with id:{file.id} is locked.')
        return super().validate(attrs)
    
    def create(self, validated_data):
        for file in self.file_list:
            file.editor=self.context['request'].user
            file.save()
        return True

    def to_representation(self, instance):
        return {}


class CheckOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'file')

    def update(self, instance, validated_data):
        validated_data['editor'] = None
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return {}
