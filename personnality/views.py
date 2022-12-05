from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from drf_yasg import openapi
from link.permissions import IsLinkedAuthenticated
from rest_framework.permissions import IsAuthenticated
from inscription.models import User
from django.http.response import JsonResponse
from controller.views import check_access_token, create_spotify_oauth
import spotipy
import envi
from spotipy.oauth2 import SpotifyOAuth


get = openapi.Parameter(
    'personnality',
    openapi.IN_QUERY,
    description="get some info about current user", 
    type=openapi.TYPE_OBJECT)

@swagger_auto_schema(
    method="get",
    manual_parameters=[get]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsLinkedAuthenticated])
def personnality(request):
    if request.method == 'GET':
        user = User.objects.get(id=request.user.id)
        user.last_url = "personnality"
        user.save()
        check_access_token(request)
        sp = create_spotify_oauth()
        SPOTIPY_CLIENT_ID=envi.SECRET_ID
        SPOTIPY_CLIENT_SECRET=envi.SECRET_PASS
        SPOTIPY_REDIRECT_URI=envi.SPOTIPY_REDIRECT_URI
        scope="user-read-playback-state, app-remote-control, user-modify-playback-state, playlist-read-private, playlist-read-private, playlist-read-collaborative, user-follow-read, user-read-currently-playing, user-read-playback-position, user-library-modify, playlist-modify-private, playlist-modify-public, user-read-email, user-top-read, streaming, user-read-recently-played, user-read-private, user-library-read"
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=SPOTIPY_REDIRECT_URI,scope=scope))
        tracks = sp.current_user_saved_tracks(limit=50)["items"]
        liked_songs = []
        data = []
        danceability = 0
        valence = 0
        nb_song = 0
        tempo = 0
        instru = 0
        vocale = 0
        for track in tracks:
            nb_song += 1
            track_uri = track["track"]["uri"]
            track_name = track["track"]["name"]
            print(track_uri)
            print(track_name)
            liked_songs.append(track["track"]["id"])
            data = sp.audio_features(track_uri)[0]
            danceability += data["danceability"]
            valence += data["valence"]
            tempo += data["tempo"]
            instru += data["instrumentalness"]
            vocale += data["speechiness"]

        if nb_song == 0:
            return JsonResponse("Aucune chanson aimée", safe=False)

        vocale = vocale / nb_song
        instru = instru / nb_song
        tempo = tempo / nb_song
        valence = valence / nb_song
        danceability = danceability / nb_song
        
        result = {
            'dance' : danceability,
            'Agitation' : tempo,
            'vocale' : vocale,
            'instru' : instru,
            'valence' : valence
        }


        return JsonResponse(result, safe=False)
