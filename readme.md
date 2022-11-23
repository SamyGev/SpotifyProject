# DjangoTify Api

## Features

### 1 - Inscription

**username** : pour le nom d'utilisateur (unique)  
**password** : haché SHA256  
  
### 2 - Connexion DjangoTify
Générer un token valide **une heure** pour accéder aux services  

### 3 - Liaison Spotify
L'utilisateur, après s'être authentifié sur notre service, s'authentifie auprès de spotify.
Spotify délègue l'authorisation à DjangoTify.

### 4 - Groups
Création de groupe en en **rejoignant** un (par le nom de groupe).  
Un utilisateur qui **créé** un groupe en devient le chef.  
Un utilisateur n'appartient qu'**un seul** groupe.
Un groupe est **détruit** s'il n'a pas d'utilisateurs

### 5 - Utilisation des groupes
#### ***Liste des groupes*** 
Un utilisateur peut consulter la liste des groupes dispo, il voit ainsi:
* Le nom du groupe
* le nombre d'utilisateurs présents  

#### ***Liste des membres du groupe*** 
Il peut aussi voir, pour **son** groupe:
* les noms des utilisateurs
* le chef du groupe 
* pseudo du compte spotify
* morceau en cours d'écoute
  * titre du morceau
  * nom de l'artiste
  * titre de l'album

### 6 - Personnalité de l'utilisateur
 Analyse des titres likés, plus précisément :
 * attrait pour la dance (note /10) - danceability
 * tempo moyen écouté - tempo
 * préférence entre les musiques vocales ou instrumentales - speechiness
 * musique positive ou négative - valence

### 7 - Synchronisation 
Le chef peut faire écouter sa musique, de façon ***synchrone et directe***, aux utilisateurs de son groupe

### 8 - Création de playlist
Un utilisateur peut créer une playlist basée sur les 10 musiques préférées d'un autre utilisateur (ça peut être lui même)

### 9 - Tests unitaires et d'integration
Les tests devront être fait

### 10 - Dockerfile
Conteneuriser l'appli, prévoir une mise en prod

### 11 - Reverse proxy
Fournir une conf permettant l'utilisation d'un reverse proxy

## Ressources
[https://www.djangoproject.com/](#)  
[https://www.django-rest-framework.org/](#)  
[https://www.https://swagger.io/.com/](#)  
[https://www.developer.spotify.com/](#)  
[https://docs.docker.com/](#)  

## BackLog
1. Inscription
2. Swagger UI
3. Connexion DjangoTify
4. Liaison Spotify
5. Groups
6. Liste des groupes
7. Liste des membres du groupe
8. Personnalité de l'utilisateur
9. Synchronisation
10. Création de playlist
11. Dockerfile
12. Reverse proxy
13. Tests unitaires et d'integration

## Environement
.\venv\Scripts\activate pour activer le venv **en integ**
Dépendances dans le **requirements.txt**

## Déploiement
### Docker
### systemd

# Endpoint
## SwaggerUI


# Notes au 15/11
* Faire la connection à l'api spotify
* Modifier le User pour implémenter la liaison (username du compte spotify, token à sauvegarder hashé)
* Créer les groupes
* Modifier le swagger 