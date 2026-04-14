from rest_framework.permissions import BasePermission
from companies.models import Membership


class IsMember(BasePermission):
    """
    Allows access only to users who are
    a member or admin of the company.
    Company ID must be in the URL kwargs as 'company_id'.
    """
    message = 'You are not a member of this company.'

    def has_permission(self, request, view):
        company_id = view.kwargs.get('company_id')
        if not company_id:
            return False
        return Membership.objects.filter(
            user=request.user,
            company_id=company_id
        ).exists()


class IsCompanyAdmin(BasePermission):
    """
    Allows access only to users who are
    admin of the company.
    Company ID must be in the URL kwargs as 'company_id'.
    """
    message = 'You must be a company admin to perform this action.'

    def has_permission(self, request, view):
        company_id = view.kwargs.get('company_id')
        if not company_id:
            return False
        return Membership.objects.filter(
            user=request.user,
            company_id=company_id,
            role=Membership.Role.ADMIN
        ).exists()