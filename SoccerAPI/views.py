from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from SoccerAPI.models import League,Club,Player
from SoccerAPI.serializer import LeagueSerializer,ClubSerializer,PlayerSerializer
from django.shortcuts import get_object_or_404

# Create your views here.

#---------------------------
#|   Views for Leagues     |
#---------------------------

class ShowLeagues(APIView):
    def get(self,request):
        leagues = League.objects.all()
        serializer = LeagueSerializer(leagues,many=True)
        return Response(serializer.data)

class AddLeagues(APIView):
    def post(self,request):
        serializer = LeagueSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else: 
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        
#---------------------------
#|   Views for Clubs       |
#---------------------------
#         
class ShowClubs(APIView):
    def get(self,request):
        clubs = Club.objects.all()
        serializer = ClubSerializer(clubs,many=True)
        return Response(serializer.data)

class ShowClubsByLeague(APIView):
    def get(self, request, league):
        try:
            league_obj = League.objects.get(name=league)
        except League.DoesNotExist:
            return Response("League not found", status=status.HTTP_404_NOT_FOUND)

        clubs = Club.objects.filter(league=league_obj)
        serializer = ClubSerializer(clubs, many=True)
        return Response(serializer.data)

class SpecificClub(APIView):
    def get(self,request,name):
        try:
            club = Club.objects.get(name = name)
        except Club.DoesNotExist:
            return Response("Club does not excist",status=status.HTTP_404_NOT_FOUND)
        serializer = ClubSerializer(club,many=False)
        return Response(serializer.data)


class AddClub(APIView):
    def post(self, request):
        league_name = request.data.get('league_name')

        league = get_object_or_404(League, name=league_name)

        serializer = ClubSerializer(data=request.data)
        if serializer.is_valid():
            club = serializer.save(league=league) 
            serializer = ClubSerializer(club)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class MoreMoney4Club(APIView):
    def put(self,request,name):
        added_money = request.data.get('money')
        added_money
        try:
            club = Club.objects.get(name=name)
        except Club.DoesNotExist:
            return Response("Club not found",status=status.HTTP_404_NOT_FOUND)
        club.budget += added_money
        club.save()
        serializer = ClubSerializer(club,many=False)
        return Response(serializer.data)


#---------------------------
#|   Views for Players     |
#---------------------------