from companies.models import Membership



class CompanyMixin:
    """
    Mixin to provide helper method to get company and membership for a user.
    Assumes company_id is in the URL kwargs as 'company_id'.
    """
    def get_membership(self, request, company_id):
        try:
            company = Membership.objects.get(
                user=request.user,
                company_id=company_id
            )
            return company
        except Membership.DoesNotExist:
            return None
        
    def is_admin(self, request, company_id):
        membership = self.get_membership(request, company_id)
        if not membership:
            return False
        
        return membership.role == Membership.Role.ADMIN