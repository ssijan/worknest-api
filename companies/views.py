from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Company, Membership
from .serializers import CompanySerializer, MemberSerializer, AddMemberSerializer
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema

from core.permissions import IsMember, IsCompanyAdmin


# Create your views here.
User = get_user_model()


def get_user_company(user, company_id):
    try:
        company = Company.objects.get(id=company_id)
        membership = Membership.objects.get(user=user, company=company)
        return company, membership
    except (Company.DoesNotExist, Membership.DoesNotExist):
        return None, None



@extend_schema(tags=['Companies'], request=CompanySerializer)
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def company_list_create(request):
    if request.method == 'GET':
        companies = Company.objects.filter(memberships__user=request.user)
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            company = serializer.save(owner=request.user)
            Membership.objects.create(user=request.user, company=company, role=Membership.Role.ADMIN)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# Endpoint to get company details (only for members)
@extend_schema(tags=['Companies'])
@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated, IsMember])
def company_detail(request, company_id):
    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        return Response({"error": "Company not found."}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CompanySerializer(company)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        membership = Membership.objects.get(user=request.user, company=company)
        if membership.role != Membership.Role.ADMIN:
            return Response({"error": "Only admins can delete the company."}, status=status.HTTP_403_FORBIDDEN)
        
        company.delete()
        return Response({"message": "Company deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    



# Endpoint to list members of a company and add new members (admin only)
@extend_schema(tags=['Companies'], request=AddMemberSerializer)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsMember])
def member_list_add(request, company_id):
    company, membership = get_user_company(request.user, company_id)
    if not company:
        return Response({"error": "Company not found or you are not a member."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        members = Membership.objects.filter(company=company).select_related('user')
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if membership.role != Membership.Role.ADMIN:
            return Response({"detail": "Only admins can add members."}, status=status.HTTP_403_FORBIDDEN)

        serializer = AddMemberSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data['email'])
            if Membership.objects.filter(user=user, company=company).exists():
                return Response({"detail": "User is already a member of this company."}, status=status.HTTP_400_BAD_REQUEST)
            
            new_member = Membership.objects.create(
                user=user,
                company=company,
                role=serializer.validated_data['role']
            )
            return Response(MemberSerializer(new_member).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

