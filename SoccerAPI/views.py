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

class AddPlayer(APIView):
    def post(self,request):
        club_name = request.data.get('club_name')
        
        club = get_object_or_404(Club,name=club_name)

        serializer = PlayerSerializer(data = request.data) 
        if serializer.is_valid():
            player = serializer.save(club = club)
            serializer = PlayerSerializer(player)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

class ShowPlayers(APIView):
    def get(self,request):
        players = Player.objects.all()
        serializer = PlayerSerializer(players,many=True)
        return Response(serializer.data)   

class getByNationality(APIView):
    def get(self,request,nation):
        try:
            player = Player.objects.filter(nationallity = nation)
        except Player.DoesNotExist:
            return Response("No player with that nationality",status=status.HTTP_404_NOT_FOUND)
        serializer = PlayerSerializer(player,many=True)
        return Response(serializer.data)
    
class getByClub(APIView):
    def get(self,request,club):
        try:
            club_obj = Club.objects.get(name = club)
        except:
            return Response('No player plays for that club',status=status.HTTP_404_NOT_FOUND)
        player = Player.objects.filter(club=club_obj)
        serializer = PlayerSerializer(player, many=True)
        return Response(serializer.data)

class TransferPlayer(APIView):
    def put(self,request):
        new_club = request.data.get('club_name')
        name_player = request.data.get('player_name')
        try:
            club_obj = Club.objects.get(name = new_club)
        except:
            return Response('There is no club with that name',status=status.HTTP_404_NOT_FOUND)
        try:
            player = Player.objects.get(last_name = name_player)
        except:
            return Response('There is no player with that name',status=status.HTTP_404_NOT_FOUND)
        
        if club_obj.budget < player.price:
            return Response('The club does not have enough money to buy the player',status=status.HTTP_401_UNAUTHORIZED)
        else:
            player.club = club_obj
            player.save()
            club_obj.budget -= player.price
            club_obj.save()
            serializer = PlayerSerializer(player,many=False)
            return Response(serializer.data)
        
      
        
