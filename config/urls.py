from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=['Health'],
    description="Simple endpoint to check if the API is running. Returns basic status information.",
    auth=[],
)
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({
        "status": "ok",
        "project": "WorkNest API",
        "version": "1.0.0"
    })

urlpatterns = [
    # API Documentation
    path('api/docs/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/',SpectacularSwaggerView.as_view(url_name='schema'),name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'),name='redoc'),

    path('admin/', admin.site.urls),
    path('api/health/', health_check),
    path('api/auth/', include('accounts.urls')),
    path('api/companies/', include('companies.urls')),  
    path('api/companies/<int:company_id>/projects/', include('projects.urls')),
    path('api/companies/<int:company_id>/projects/<int:project_id>/tasks/', include('tasks.urls')),
    path('api/', include('core.urls')),



]
