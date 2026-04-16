from django.urls import path
from . import views


urlpatterns = [
    path('companies/<int:company_id>/activity/', views.company_activity, name='company-activity'),
    path('companies/<int:company_id>/projects/<int:project_id>/activity/', views.project_activity, name='project-activity'),
]