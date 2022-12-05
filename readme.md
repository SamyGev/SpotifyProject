# DjangoTify Api

## Features

### 1 - Inscription

POST /inscription/
  * username  
  * password1  
  * password2
  
### 2 - Connexion DjangoTify

POST /connection/login  
* username
* password    
  
token valide **1 heure**  
Utilisation de django-all-auth (possibilité de se connecter avec facebook...etc en SSO, mais pas testé par manque de temps)

### 3 - Liaison Spotify

GET /link/

On lie notre compte, on récupère un token qu'on stocke dans la base, ainsi que le nom spotify, on est prêt à utiliser notre API

### 4 - Groupes

POST /groups 
* group_name

DELETE /groups
* group_name


### 5 - Utilisation des groupes
#### ***Liste des groupes GET /groups/***  
Un utilisateur peut consulter la liste des groupes dispo, il voit ainsi:
* Le nom du groupe
* le nombre d'utilisateurs présents  

#### ***Liste des membres du groupe GET /groups/<slug>/*** 
Il peut aussi voir, pour **son** groupe:
* les noms des utilisateurs
* le chef du groupe 
* pseudo du compte spotify
* morceau en cours d'écoute
  * titre du morceau
  * nom de l'artiste
  * titre de l'album

### 6 - Personnalité de l'utilisateur GET /personnality/
 Analyse des titres likés, plus précisément :
 * attrait pour la dance (note /10) - danceability
 * tempo moyen écouté - tempo
 * préférence entre les musiques vocales ou instrumentales - speechiness
 * musique positive ou négative - valence

### 7 - Synchronisation GET /synchronization/
Le chef peut faire écouter sa musique, de façon ***synchrone et directe***, aux utilisateurs de son groupe

### 8 - Création de playlist POST /playlist/
Un utilisateur peut créer une playlist basée sur les 10 musiques préférées d'un autre utilisateur (ça peut être lui même)

### 9 - Tests unitaires et d'integration
Les tests devront être fait

### 10 - Dockerfile
Conteneuriser l'appli, c'est fait, le dockerfile est très simple, pas de volume de données.  
* On récupère python:3.10.8
* On set notre workdir de manière conventionnelle /usr/src/app  
* On prend notre environnement virtuel requis
* On installe les dépendances
* On copie nos fichiers
* On lance le serveur (0.0.0.0:8000)
* On expose le port 8000

### 11 - Reverse proxy - PAS FAIT
Fournir une conf permettant l'utilisation d'un reverse proxy

## Ressources
[https://www.youtube.com/](#)  
[https://www.djangoproject.com/](#)  
[https://www.django-rest-framework.org/](#)  
[https://www.https://swagger.io/.com/](#)  
[https://www.developer.spotify.com/](#)  
[https://docs.docker.com/](#)  

## BackLog
1. Inscription - OK
2. Swagger UI - OK
3. Dockerfile - OK
4. Connexion DjangoTify - OK
5. Liaison Spotify - OK
6. Groupes - OK
7. Liste des groupes - OK
8. Liste des membres du groupe - OK
9. Personnalité de l'utilisateur - OK
10.  Synchronisation - OK - à test
11. Création de playlist -
12. Reverse proxy - PAS FAIT
13. Tests unitaires et d'integration - PAS FAIT

## Environement
.\venv\Scripts\activate pour activer le venv **en integ** (Ou on instancie un contenair)
Dépendances dans le **requirements.txt**

## SwaggerUI /swagger/
Peut être utiliser, manque surement de test et j'aurais pu virer les endpoints que je n'ai pas exploré (surtout sur l'authentification avec all-auth)

# Projet
## Décomposition du projet
Je savais que j'allais partir sur du python (le langage me semble complet, simple, et puissant avec ses librairies et sa communauté).  
La première étape consistait à faire le plan de développement, l'architecture de l'application, décomposée en microservices.  
Nous avons donc : 
* controller (classique, nos settings, et quelques utilitaires)
* groups (et notre model Groups) 
* inscription (et notre model User surchargé)
* link
* personnality
* playlist
* spotify_api (avec seulement quelques utilitaires)

Une fois le projet bien défini, j'ai fait un backlog très simple. Pour démarrer en autonomie, il fallait que j'arrive à faire valider mon architecture, et que j'arrive à terminer ***l'inscription, le dockerfile, et le swagger***.

## Répartition de la charge
Je suis seul :)   
Mais globalement, je me suis occupé d'un maximum de choses en solo, sans demander de l'aide à la communauté (StackOverflow).  
Ca m'a surtout desservi car j'ai rencontré un sérieux problème sur ma fonction de callback, que j'ai sû résoudre en fouillant pas mal sur github.

## Documentation
Ma priorité #1 était de commencer le projet avec la FT1, documenté est un swagger UI implémenté.
Même s'il n'est surement pas parfait, il couvre bien mes besoins et faire ça au fur et a mesure du développement était plus aisé.

## Production de documents
Je travail presque essentiellement avec la documentation de la technologie que j'utilise, si ça ne suffit pas, je vais sur Stack Overflow / Youtube, ensuite, je fais des schémas papiers, et si ça ne suffit pas, je vais sur github ou je créé un post Stack Overflow.