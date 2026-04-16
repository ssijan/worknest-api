from .models import ActivityLog

# Helper function to save activity logs
def log_activity(company, actor, action, description='', extra_data=None):
    
    ActivityLog.objects.create(
        company=company,
        actor=actor,
        action=action,
        description=description,
        extra_data=extra_data or {}
    )