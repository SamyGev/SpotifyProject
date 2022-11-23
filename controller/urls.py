"""SpotifyProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view as schema

schema_view = schema(
    openapi.Info(
        title="API Description",
        default_version="1.0",
        description="Description de l'API DjangoTify et des endpoints exposés",
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inscription/', include('inscription.urls')),
    path('connection/', include('connection.urls')),
    path('groups/', include('groups.urls')),
    path('link/', include('link.urls')),
    path('personnality/', include('personnality.urls')),
    path('playlist/', include('playlist.urls')),
    path('synchronization/', include('synchronization.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-schema"),
]
