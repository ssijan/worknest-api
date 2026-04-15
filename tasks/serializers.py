from rest_framework import serializers
from .models import Task
from django.contrib.auth import get_user_model
from companies.models import Membership


User = get_user_model()

class TaskSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.CharField(
        source = 'assigned_to.name',
        read_only = True
    )
    assigned_to_email = serializers.EmailField(
        source = 'assigned_to.email',
        read_only = True
    )
    created_by_name = serializers.CharField(
        source = 'created_by.name',
        read_only = True
    )
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        source = 'assigned_to',
        write_only = True,
        allow_null = True,
        required = False
    )

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description',
            'status', 'priority', 'due_date',
            'assigned_to_id', 'assigned_to_name',
            'assigned_to_email', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_assigned_to_id(self, user):
        request = self.context.get('request')
        company_id = self.context.get('company_id')
        if user and company_id:
            is_member = Membership.objects.filter(
                user=user,
                company_id=company_id
            ).exists()
            if not is_member:
                raise serializers.ValidationError('Assigned user must be a member of the company.')
        return user
    

class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status']

        
  
