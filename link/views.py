from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http.response import JsonResponse
from rest_framework import permissions
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import envi
import requests
# Create your views here.

test_param = openapi.Parameter('test', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_BOOLEAN)

@swagger_auto_schema(
    method="get",
    manual_parameters=[test_param]
)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def test(request):
    if request.method == 'GET': 
        test = "test " + request.user.username
        # scope = "user-read-private"
        # sp = getScope(scope)
        # print(sp.current_user())
        urn = 'spotify:artist:3jOstUTkEu2JkjvRdBA5Gu'
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=envi.SECRET_ID, client_secret=envi.SECRET_PASS, redirect_uri=envi.SPOTIPY_REDIRECT_URI))

        artist = sp.artist(urn)
        print(artist)

        user = sp.current_user()
        print(user)
        return JsonResponse(test, safe=False)


def getScope(spotipyScope):
# def getScope():
    # auth_manager = SpotifyClientCredentials(client_id=envi.SECRET_ID, client_secret=envi.SECRET_PASS)
    # sp = spotipy.Spotify(auth_manager=auth_manager)
    token = SpotifyOAuth(scope=spotipyScope,client_id=envi.SECRET_ID, client_secret=envi.SECRET_PASS, redirect_uri=envi.SPOTIPY_REDIRECT_URI)
    spotifyObject = spotipy.Spotify(auth_manager= token)
    return spotifyObject