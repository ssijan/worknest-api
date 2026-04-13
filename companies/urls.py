from django.urls import path
from . import views

urlpatterns = [
    path('', views.company_list_create, name='company-list-create'),
    path('<int:company_id>/', views.company_detail, name='company-detail'),
    path('<int:company_id>/members/', views.member_list_add, name='member-list-add'),
]

