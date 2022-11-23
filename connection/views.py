from django.contrib.auth import get_user_model, login
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from requests import Response
from rest_framework import permissions
from rest_framework.authentication import BasicAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer

from inscription.serializers import UserSerializer

User = get_user_model()
from knox.auth import TokenAuthentication

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token = AuthToken.objects.create(user)[1]

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,  # Get serialized User data
            "token": token
        })

class LoginView(KnoxLoginView):
    authentication_classes = [TokenAuthentication]
    permission_classes = ()