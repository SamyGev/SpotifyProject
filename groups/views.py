from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from drf_yasg import openapi
from link.permissions import IsLinkedAuthenticated
from rest_framework.permissions import IsAuthenticated
from .permissions import IsGroupedAuthenticated
from inscription.models import User
from spotify_api.models import SpotifyToken
from .models import Groups
from django.http.response import JsonResponse
import random
from .serializers import GroupSerializer
# Create your views here.


post = openapi.Parameter(
    'groups',
    openapi.IN_QUERY,
    description="create or join a group", 
    type=openapi.TYPE_OBJECT)
delete = openapi.Parameter(
    'groups',
    openapi.IN_QUERY,
    description="leave a group", 
    type=openapi.TYPE_OBJECT)
get = openapi.Parameter(
    'groups',
    openapi.IN_QUERY,
    description="get groups collection", 
    type=openapi.TYPE_OBJECT)


@swagger_auto_schema(
    method="get",
    manual_parameters=[get]
)
@swagger_auto_schema(
    method="post",
    manual_parameters=[post]
)
@swagger_auto_schema(
    method="delete",
    manual_parameters=[delete]
)
@api_view(['POST', 'DELETE', 'GET'])
@permission_classes([IsAuthenticated, IsLinkedAuthenticated])
def groups(request):
    if request.method == 'POST':
        user = User.objects.get(id= request.user.id)
        user.last_url = 'groups'
        user.save()
        #On veut rejoindre un groupe, ou en créer un
        need_swap = True

        #Si l'utilisateur est déjà groupé
        if is_grouped(user):
            if Groups.objects.get(id=user.group).name != request.POST.get("group_name"): 
                quit_group(user, request) #On quitte
                user = User.objects.get(id= request.user.id)
                need_swap = True
            else:
                need_swap = False
                return JsonResponse("Pas besoin de changer de groupe! :)", safe=False)
        if need_swap == True:
            #Utilisateur non groupé
            if group_exist(request): #Si le groupe existe déjà
                join_group(request)#On rejoint simplement
                user = User.objects.get(id= request.user.id)
                return JsonResponse("Groupe rejoint!", safe=False)
            else:
                create_group(request)#On créé le groupe
                return JsonResponse("Groupe créé!", safe=False)

    if request.method == 'DELETE':
        user = User.objects.get(id= request.user.id)
        user.last_url = 'groups'
        user.save()
        if is_grouped(user):
            if Groups.objects.get(id=user.group).name == request.POST.get("group_name"): 
                quit_group(user, request) #On quitte
                return JsonResponse("Groupe quitté!", safe=False)
            else:
                return JsonResponse("User pas dans le groupe!", safe=False)
        else:
            return JsonResponse("User non groupé!", safe=False)

    if request.method == 'GET':
        user = User.objects.get(id= request.user.id)
        user.last_url = 'groups'
        user.save()

        groups = Groups.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return JsonResponse(serializer.data, safe=False)

def is_grouped(user):
    if user.group == 0:
        return False
    return True

def create_group(request):
    group = Groups.objects.create(
        name= request.POST.get("group_name"),
        owner= request.user.id,
        users_amount= 1
    )
    user = User.objects.get(id= request.user.id)
    user.group = group.id
    user.save()

def join_group(request):
    group = Groups.objects.get(name= request.POST.get("group_name"))
    user = User.objects.get(id= request.user.id)
    user.group = group.id
    group.users_amount += 1
    group.save()
    user.save()

def group_exist(request):
    groups = Groups.objects.all()
    for group in groups:
        if group.name == request.POST.get("group_name"):
            return True
    return False

def quit_group(user, request):
    group = Groups.objects.get(id=user.group) 
    if group.users_amount <= 1:
        group.delete()
    else:
        #Si l'user est le chef et qu'il quitte
        if group.owner == user.id:
            future_owners = []
            for all_user in User.objects.all():#Pour chaque user
                if is_grouped(all_user):#l'user est groupé
                    if all_user.group == group.id:#C'est le bon groupe
                        if all_user.id != request.user.id: #C'est pas l'user
                            future_owners.append(all_user.id)
            group.owner = random.choice(future_owners) #Chaque user devient chef s'il fait parti du groupe
            group.save()
        group.users_amount -= 1
        group.save()
    user.group = 0
    user.save()



get = openapi.Parameter(
    'group_members',
    openapi.IN_QUERY,
    description="get info from users in the same group", 
    type=openapi.TYPE_OBJECT)


@swagger_auto_schema(
    method="get",
    manual_parameters=[get]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsLinkedAuthenticated, IsGroupedAuthenticated])
def group_members(request, group_name):
    if request.method == 'GET':
        user = User.objects.get(id= request.user.id)
        user.last_url = 'group_members'
        user.save()
        try:
            group = Groups.objects.get(name=group_name)
        except:
            return JsonResponse("Requête incorrecte! (:", safe=False, json_dumps_params={'ensure_ascii': False})

        if group.id != request.user.group or request.user.group == 0:
            return JsonResponse("Vous n'êtes pas dans ce groupe! :(", safe=False, json_dumps_params={'ensure_ascii': False})
        users = User.objects.all()
        tokens = SpotifyToken.objects.all()
        result = []
        for user in users:#Chaque user
            for token in tokens:#Chaque token (spotify nom)
                if token.user_id == user.id:
                    if request.user.group == user.group:#Si on est dans le même groupe
                        if user.id == group.owner:
                            result.append({
                                "nom_DjangoTify":user.username,
                                "nom_Spotify":token.username,
                                "chef":"oui",
                                "ecoute_actuellement":None,
                                "sur_l_appareil":None
                            })
                        else:
                            result.append({
                                "nom_DjangoTify":user.username,
                                "nom_Spotify":token.username,
                                "chef":"non",
                                "ecoute_actuellement":None,
                                "sur_l_appareil":None
                            })
        return JsonResponse(result, safe=False)