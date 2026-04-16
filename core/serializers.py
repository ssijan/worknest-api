from rest_framework import serializers
from .models import ActivityLog


class ActivityLogSerializer(serializers.ModelSerializer):
    actor_name = serializers.CharField(
        source = 'actor.name',
        read_only = True
    )
    actor_email = serializers.EmailField(
        source = 'actor.email',
        read_only = True
    )

    class Meta:
        model = ActivityLog
        fields = [
            'id', 'action', 'description',
            'actor_name', 'actor_email',
            'extra_data', 'created_at'
        ]
        read_only_fields = fields