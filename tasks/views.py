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
        task = Task.objects.filter(project=project).select_related('assigned_to', 'created_by')
        serializer = TaskSerializer(task, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = TaskSerializer(
            data=request.data,
            context={'request': request, 'company_id': company_id}
        )
        if serializer.is_valid():
            serializer.save(project=project, created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


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
        serializer = TaskSerializer(
            task,
            data = request.data,
            partial = True,
            context={'request': request, 'company_id': company_id}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        is_member = Membership.objects.filter(
            user=request.user,
            company_id=company_id,
            role=Membership.Role.ADMIN
        ).exists()
        if not is_member:
            return Response({'error': 'Only company admins can delete tasks.'}, status=status.HTTP_403_FORBIDDEN)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsMember])
def task_status_update(request, company_id, project_id, task_id):
    project = get_project_or_404(company_id, project_id)
    if not project:
        return Response({'error': 'Project not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    task = get_task_or_404(project, task_id)
    if not task:
        return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = TaskStatusSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)