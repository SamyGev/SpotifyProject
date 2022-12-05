from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from requests import Response
from rest_framework.decorators import api_view, permission_classes
from drf_yasg import openapi
from .permissions import IsGroupChief
from link.permissions import IsLinkedAuthenticated
from rest_framework.permissions import IsAuthenticated
from inscription.models import User
from groups.models import Groups
from spotify_api.models import SpotifyToken
from django.http.response import JsonResponse
from django.forms.models import model_to_dict
import random
from rest_framework import status
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.core import serializers
from controller.views import callback, check_access_token, create_spotify_oauth
import spotipy
import envi
from spotipy.oauth2 import SpotifyOAuth
import json


get = openapi.Parameter('test delete', openapi.IN_QUERY, description="test delete manual param", type=openapi.TYPE_BOOLEAN)

@swagger_auto_schema(
    method="get",
    manual_parameters=[get]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsLinkedAuthenticated, IsGroupChief])
def synchronization(request):
    if request.method == 'GET':
        ##  /me/player/devices?
        users = User.objects.all()
        tokens = SpotifyToken.objects.all()
        groups = Groups.objects.all()
        me = User.objects.get(id=request.user.id)
        group_id = 0
        for group in groups: #Pour chaque groupe
            if me.id == group.owner: #Si je suis le chef
                group_id = group.id #Je récupère l'id du groupe
        
        check_access_token(request)
        sp = create_spotify_oauth()
        SPOTIPY_CLIENT_ID=envi.SECRET_ID
        SPOTIPY_CLIENT_SECRET=envi.SECRET_PASS
        SPOTIPY_REDIRECT_URI=envi.SPOTIPY_REDIRECT_URI
        scope="user-read-playback-state, app-remote-control, user-modify-playback-state, playlist-read-private, playlist-read-private, playlist-read-collaborative, user-follow-read, user-read-currently-playing, user-read-playback-position, user-library-modify, playlist-modify-private, playlist-modify-public, user-read-email, user-top-read, streaming, user-read-recently-played, user-read-private, user-library-read"
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=SPOTIPY_REDIRECT_URI,scope=scope))
        track = sp.currently_playing()
        progress_ms = track["progress_ms"]
        uri = track["item"]["uri"]

        for user in users: #Pour chaque user
            if user.group == group_id: #Si l'user est dans le même groupe
                for token in tokens: #On check les tokens pour trouver le sien
                    if token.user_id == user.id:
                        sp = create_spotify_oauth()
                        sp = spotipy.Spotify(auth=token.access_token)
                        device = sp.devices()
                        sp.add_to_queue(uri)
                        sp.next_track()
                        sp.seek_track(progress_ms)

    return JsonResponse("Normalement c'est ok, mais faut vérifier :/", safe=False)

