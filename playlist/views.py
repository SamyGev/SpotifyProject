from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from drf_yasg import openapi
from groups.views import is_grouped
from link.permissions import IsLinkedAuthenticated
from rest_framework.permissions import IsAuthenticated
from inscription.models import User
from spotify_api.models import SpotifyToken
from controller.views import check_access_token, create_spotify_oauth
import spotipy
import envi
from spotipy.oauth2 import SpotifyOAuth


post = openapi.Parameter(
    'get_user_songs',
    openapi.IN_QUERY,
    description="Create a playlist from a user's member of your group", 
    type=openapi.TYPE_OBJECT)

@swagger_auto_schema(
    method="post",
    manual_parameters=[post]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsLinkedAuthenticated])
def get_user_songs(request):
    if request.method == 'POST':
        user = User.objects.get(id= request.user.id)
        tokens = SpotifyToken.objects.all()
        user.last_url = 'get_user_songs'
        user.save()
        if is_grouped(user): #Si on est groupé, et que c'est le même nom de groupe que la requete
            target = User.objects.get(id=request.POST.get("user_id"))
            if user.group == target.group:
                for token in tokens: #On check les tokens pour trouver le sien
                    if token.user_id == target.id:
                        sp = create_spotify_oauth()
                        sp = spotipy.Spotify(auth=token.access_token)
                        tracks = sp.current_user_top_tracks(limit=10)

                check_access_token(request)
                sp = create_spotify_oauth()
                SPOTIPY_CLIENT_ID=envi.SECRET_ID
                SPOTIPY_CLIENT_SECRET=envi.SECRET_PASS
                SPOTIPY_REDIRECT_URI=envi.SPOTIPY_REDIRECT_URI
                scope="user-read-playback-state, app-remote-control, user-modify-playback-state, playlist-read-private, playlist-read-private, playlist-read-collaborative, user-follow-read, user-read-currently-playing, user-read-playback-position, user-library-modify, playlist-modify-private, playlist-modify-public, user-read-email, user-top-read, streaming, user-read-recently-played, user-read-private, user-library-read"
                sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=SPOTIPY_REDIRECT_URI,scope=scope))
                tracks = sp.user_playlist_create()
