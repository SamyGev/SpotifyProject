from rest_framework.permissions import BasePermission
from spotify_api.models import SpotifyToken

# Si on est admin
class IsLinkedAuthenticated(BasePermission):
    def has_permission(self, request, view):
        tokens = SpotifyToken.objects.all()
        my_token = ""
        for token in tokens:
            if token.user_id == request.user.id:
                return True
        if my_token == "":
            return False