from rest_framework import serializers
from SoccerAPI.models import League,Club,Player
from django.forms import ValidationError

# Serializing the data from Complex Data to the data desired

class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = '__all__'
        
class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = '__all__'

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'