from rest_framework.permissions import BasePermission
from groups.models import Groups

# Si on est admin
class IsGroupChief(BasePermission):
    def has_permission(self, request, view):
        for group in Groups.objects.all():
            if group.owner == request.user.id:
                return True
        return False