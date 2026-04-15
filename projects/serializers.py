from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(
        source = 'created_by.name',
        read_only = True
    )
    created_by_email = serializers.EmailField(
        source = 'created_by.email',
        read_only = True
    )
    task_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'status',
            'created_by_name', 'created_by_email',
            'task_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    
    def get_task_count(self, obj):
        try:
            return obj.tasks.count()
        except AttributeError:
            return 0
    

class ProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description', 'status']
