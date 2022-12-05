from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Groups
class GroupSerializer(ModelSerializer):
    nom = serializers.CharField(source='name')
    nombre_d_utilisateurs = serializers.CharField(source='users_amount')

    class Meta:
        model = Groups
        fields = ['nom', 'nombre_d_utilisateurs']
