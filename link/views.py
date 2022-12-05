import envi
import spotipy
from controller.views import callback, check_access_token, create_spotify_oauth
from django.http.response import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from inscription.models import User
# Create your views here.
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from spotify_api.models import SpotifyToken
from spotipy.oauth2 import SpotifyOAuth



get = openapi.Parameter(
    'link',
    openapi.IN_QUERY,
    description="Link spotify account, set username and save or refresh token", 
    type=openapi.TYPE_OBJECT)

@swagger_auto_schema(
    method="get",
    manual_parameters=[get]
)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def link(request):
    if request.method == 'GET':
        my_token = ""
        access_token = ""
        user = User.objects.get(id=request.user.id)
        user.last_url = "link"
        user.save()
        tokens = SpotifyToken.objects.all()
        for token in tokens:
            if token.user_id == request.user.id:
                my_token = token
                access_token = token.access_token
                check_access_token(request)
        
        if access_token != "" :
            sp = spotipy.Spotify(auth=access_token)
            return JsonResponse(my_token.username, safe=False)
        else:
            sp = create_spotify_oauth()
            callback(request._request)
            SPOTIPY_CLIENT_ID=envi.SECRET_ID
            SPOTIPY_CLIENT_SECRET=envi.SECRET_PASS
            SPOTIPY_REDIRECT_URI=envi.SPOTIPY_REDIRECT_URI
            scope="user-read-playback-state, app-remote-control, user-modify-playback-state, playlist-read-private, playlist-read-private, playlist-read-collaborative, user-follow-read, user-read-currently-playing, user-read-playback-position, user-library-modify, playlist-modify-private, playlist-modify-public, user-read-email, user-top-read, streaming, user-read-recently-played, user-read-private, user-library-read"
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=SPOTIPY_REDIRECT_URI,scope=scope))
            return JsonResponse(sp.current_user()["display_name"], safe=False)