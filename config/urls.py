"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
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
    path('admin/', admin.site.urls),
    path('api/health/', health_check),
    path('api/auth/', include('accounts.urls')),
    path('api/companies/', include('companies.urls')),  
    path('api/companies/<int:company_id>/projects/', include('projects.urls')),
    path('api/companies/<int:company_id>/projects/<int:project_id>/tasks/', include('tasks.urls')),
    path('api/', include('core.urls')),

    # API schema and docs
    path('api/docs/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(), name='swagger'),
    path('api/docs/redoc/', SpectacularSwaggerView.as_view(url_name='schema'), name='redoc'),

]
