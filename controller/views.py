import datetime
from django.http import JsonResponse
import pytz
import envi
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.decorators import api_view
from spotify_api.models import SpotifyToken
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(
    method="get",
    auto_schema=None
)
@api_view(['GET'])
def callback(request, format=None):
    if request.method == 'GET':
        sp_oauth = create_spotify_oauth()
        code = request.GET.get('code')
        token_info = sp_oauth.get_access_token(code)
        date = datetime.datetime.now() + datetime.timedelta(hours=1)
        token = SpotifyToken(
            access_token=token_info['access_token'],
            refresh_token=token_info["refresh_token"], 
            token_type=token_info['token_type'], 
            expires_in=date, 
            user_id=request.user.id,
            username=spotipy.Spotify(auth=token_info['access_token']).current_user()["display_name"]
            )
        token.save()
        return redirect(reverse(request.user.last_url))

@swagger_auto_schema(
    method="get",
    auto_schema=None
)
@api_view(['GET'])
def home(request):
    if request.method == 'GET':
        print('on est sur home')
        return JsonResponse("Home :)", safe=False)
        

def create_spotify_oauth():
    return SpotifyOAuth(
            client_id=envi.SECRET_ID,
            client_secret=envi.SECRET_PASS,
            redirect_uri=envi.SPOTIPY_REDIRECT_URI,
            scope="user-read-playback-state, app-remote-control, user-modify-playback-state, playlist-read-private, playlist-read-private, playlist-read-collaborative, user-follow-read, user-read-currently-playing, user-read-playback-position, user-library-modify, playlist-modify-private, playlist-modify-public, user-read-email, user-top-read, streaming, user-read-recently-played, user-read-private, user-library-read")

def check_access_token(request):
    utc=pytz.UTC
    date = utc.localize(datetime.datetime.now())
    tokens = SpotifyToken.objects.all()
    my_token = ""
    for token in tokens:
        if token.user_id == request.user.id:
            my_token = token
            print(token.expires_in)
            print("------------------")
    if my_token == "":
        print("no token found")
    else:
        if token.expires_in < date:
            SpotifyToken.objects.get(id = my_token.id).delete()
            sp_oauth = create_spotify_oauth()
            code = request.GET.get('code')
            token_info = sp_oauth.get_access_token(code)
            date = datetime.datetime.now() + datetime.timedelta(hours=1)
            my_token = SpotifyToken(
                access_token=token_info['access_token'],
                refresh_token=token_info["refresh_token"], 
                token_type=token_info['token_type'], 
                expires_in=date, 
                user_id=request.user.id)
            my_token.save()
            return redirect(reverse(request.user.last_url))
        else:
            print("token is still good to use")

def get_token():
    return redirect(reverse('callback'))

