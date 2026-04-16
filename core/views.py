from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from .models import ActivityLog
from .serializers import ActivityLogSerializer
from .pagination import StandardPagination
from .permissions import IsMember
from companies.models import Company
from projects.models import Project


# Create your views here.

@extend_schema(tags=['Activity'])
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsMember])
def company_activity(request, company_id):
    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)

    logs = ActivityLog.objects.filter(company=company).select_related('actor')
    paginator = StandardPagination()
    paginated_logs = paginator.paginate_queryset(logs, request)
    serializer = ActivityLogSerializer(paginated_logs, many=True)
    return paginator.get_paginated_response(serializer.data)


@extend_schema(tags=['Activity'])
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsMember])
def project_activity(request, company_id, project_id):
    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        project = Project.objects.get(id=project_id, company=company)
    except Project.DoesNotExist:
        return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

    logs = ActivityLog.objects.filter(
        company=company,
        extra_data__project_id=project.id
    ).select_related('actor')

    paginator = StandardPagination()
    paginated_logs = paginator.paginate_queryset(logs, request)
    serializer = ActivityLogSerializer(paginated_logs, many=True)
    return paginator.get_paginated_response(serializer.data)
