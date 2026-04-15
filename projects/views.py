from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Project
from .serializers import ProjectSerializer, ProjectUpdateSerializer
from companies.models import Company, Membership
from core.permissions import IsCompanyAdmin, IsMember

# Create your views here.


def get_company_or_404(company_id):
    try:
        return Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        return None
    

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsMember])
def project_list(request, company_id):
    company = get_company_or_404(company_id)
    if not company:
        return Response({'error': 'Company not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        projects = Project.objects.filter(company=company).select_related('created_by')
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=company, created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated, IsMember])
def project_detail(request, company_id, project_id):
    company = get_company_or_404(company_id)
    if not company:
        return Response({'error': 'Company not found.'}, status=status.HTTP_404_NOT_FOUND)

    try:
        project = Project.objects.get(id=project_id, company=company)
    except Project.DoesNotExist:
        return Response({'error': 'Project not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = ProjectUpdateSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        membership = Membership.objects.get(
            user=request.user,
            company=company
        )
        if membership.role != Membership.Role.ADMIN:
            return Response(
                {'error': 'Only admins can delete projects'},
                status=status.HTTP_403_FORBIDDEN
            )
        project.delete()
        return Response(
            {'message': 'Project deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )