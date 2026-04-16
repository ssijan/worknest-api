from django.db import models
from django.conf import settings
from companies.models import Company

# Create your models here.


class ActivityLog(models.Model):
    class Action(models.TextChoices):
        TASK_CREATED = 'task_created', 'Task Created'
        TASK_UPDATED = 'task_updated', 'Task Updated'
        TASK_STATUS_CHANGED = 'task_status_changed', 'Task Status Changed'
        TASK_ASSIGNED = 'task_assigned', 'Task Assigned'
        TASK_DELETED = 'task_deleted', 'Task Deleted'
        PROJECT_CREATED = 'project_created', 'Project Created'
        PROJECT_UPDATED = 'project_updated', 'Project Updated'
        PROJECT_DELETED = 'project_deleted', 'Project Deleted'
        MEMBER_ADDED = 'member_added', 'Member Added'

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='activity_logs')
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='activity_logs'
    )
    
    action = models.CharField(max_length=50, choices=Action.choices)
    description = models.TextField(blank=True)
    extra_data = models.JSONField(
        default=dict,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.actor} performed {self.action} at {self.created_at}"
    

