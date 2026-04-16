from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from .models import Task
from .serializers import TaskSerializer, TaskStatusSerializer
from core.permissions import IsCompanyAdmin, IsMember
from companies.models import Membership
from projects.models import Project
from .filters import TaskFilter
from core.pagination import StandardPagination
from companies.models import Company
from core.models import ActivityLog
from core.activity import log_activity

# Create your views here.

def get_project_or_404(company_id, project_id):
    try:
        return Project.objects.get(id=project_id, company_id=company_id)
    except Project.DoesNotExist:
        return None
    
def get_task_or_404(project, task_id): 
    try:
        return Task.objects.get(id=task_id, project=project)
    except Task.DoesNotExist:
        return None


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsMember])
def task_list_create(request, company_id, project_id):
    project = get_project_or_404(company_id, project_id)
    if not project:
        return Response({'error': 'Project not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        tasks = Task.objects.filter(project=project).select_related('assigned_to', 'created_by')

        # Apply filters
        task_filter = TaskFilter(request.GET, queryset=tasks)
        tasks = task_filter.qs

        # Apply search
        search = request.GET.get('search')
        if search:
            tasks = tasks.filter(title__icontains=search)           

        # Apply ordering
        ordering = request.GET.get('ordering')
        allowable_ordering_fields = [
            'created_at', '-created_at',
            'due_date', '-due_date',
            'priority', '-priority',
        ]
        if ordering in allowable_ordering_fields:
            tasks = tasks.order_by(ordering)

        # Apply pagination
        paginator = StandardPagination()
        paginated_tasks = paginator.paginate_queryset(tasks, request)
        serializer = TaskSerializer(paginated_tasks, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    elif request.method == 'POST':
        serializer = TaskSerializer(
            data=request.data,
            context={'request': request, 'company_id': company_id}
        )

        serializer.is_valid(raise_exception=True)
        task = serializer.save(project=project, created_by=request.user)

        log_activity(
            company=project.company,
            actor=request.user,
            action=ActivityLog.Action.TASK_CREATED,
            description=f"{request.user.name} created task '{task.title}' in project '{project.name}'",
            extra_data={
                'task_id': task.id,
                'task_title': task.title,
                'project_id': project.id,
                'project_name': project.name
            }
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated, IsMember])
def task_detail(request, company_id, project_id, task_id):
    project = get_project_or_404(company_id, project_id)
    if not project:
        return Response({'error': 'Project not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    task = get_task_or_404(project, task_id)
    if not task:
        return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    
    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        old_assigned = task.assigned_to
        serializer = TaskSerializer(
            task,
            data = request.data,
            partial = True,
            context={'request': request, 'company_id': company_id}
        )

        serializer.is_valid(raise_exception=True)
        updated_task = serializer.save()
        
        if old_assigned != updated_task.assigned_to and updated_task.assigned_to:
            log_activity(
                company=project.company,
                actor=request.user,
                action=ActivityLog.Action.TASK_ASSIGNED,
                description=f"{request.user.name} assigned task '{task.title}' to {updated_task.assigned_to.name}",
                extra_data={
                    'task_id': task.id,
                    'task_title': task.title,
                    'project_id': project.id,
                    'assigned_to_name': updated_task.assigned_to.name
                }
            )
        else:
            log_activity(
                company=company,
                actor=request.user,
                action=ActivityLog.Action.TASK_UPDATED,
                description=f"{request.user.name} updated task '{task.title}'",
                extra_data={
                    'task_id': task.id,
                    'task_title': task.title,
                    'project_id': project.id
                }
            )

        return Response(serializer.data)

    elif request.method == 'DELETE':
        is_member = Membership.objects.filter(
            user=request.user,
            company_id=company_id,
            role=Membership.Role.ADMIN
        ).exists()
        if not is_member:
            return Response({'error': 'Only company admins can delete tasks.'}, status=status.HTTP_403_FORBIDDEN)
        
        company = Company.objects.get(id=company_id)
        log_activity(
            company=company,
            actor=request.user,
            action=ActivityLog.Action.TASK_DELETED,
            description=f"{request.user.name} deleted task '{task.title}' from project '{project.name}'",
            extra_data={
                'task_title': task.title,
                'project_id': project.id,
                'project_name': project.name
            }
        )
        
        task.delete()

        return Response({'message': 'Task deleted successfully.'}, status=status.HTTP_200_OK)
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsMember])
def task_status_update(request, company_id, project_id, task_id):
    project = get_project_or_404(company_id, project_id)
    if not project:
        return Response({'error': 'Project not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    task = get_task_or_404(project, task_id)
    if not task:
        return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    old_status = task.status
    serializer = TaskStatusSerializer(task, data=request.data, partial=True)
    
    serializer.is_valid(raise_exception=True)
    serializer.save()

    log_activity(
        company=project.company,
        actor=request.user,
        action=ActivityLog.Action.TASK_STATUS_CHANGED,
        description=f"{request.user.name} changed status of task '{old_status}' to '{task.status}'",
        extra_data={
            'task_id': task.id,
            'task_title': task.title,
            'project_id': project.id,
            'old_status': old_status,
            'new_status': task.status
        }
    )

    return Response(serializer.data)
