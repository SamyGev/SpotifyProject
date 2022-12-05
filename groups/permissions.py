from rest_framework.permissions import BasePermission
from .models import Groups
from django.http.response import JsonResponse
# Si on est admin
class IsGroupedAuthenticated(BasePermission):
    def has_permission(self, request, view):
        try:
            group = Groups.objects.get(name= request.GET.get("group_name"))
        except:
            return JsonResponse("Groupe inexistant!", safe=False)
        return bool(request.user and request.user.is_authenticated and (request.user.group == group.id))