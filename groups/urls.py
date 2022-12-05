from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
        path('', views.groups, name='groups'),
        path('<slug:group_name>/', views.group_members, name='group_members'),
]

urlpatterns = format_suffix_patterns(urlpatterns)