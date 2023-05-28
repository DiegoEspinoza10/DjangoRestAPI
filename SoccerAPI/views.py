from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from SoccerAPI.models import League,Club,Player,User
from SoccerAPI.serializer import LeagueSerializer,ClubSerializer,PlayerSerializer,UserSerializer
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
        added_money = added_money.split('M')[0]
        toadd = int(added_money)
        try:
            club = Club.objects.get(name=name)
        except Club.DoesNotExist:
            return Response(added_money,status=status.HTTP_404_NOT_FOUND)
        
        money_of_club = club.budget
        money_of_club = money_of_club.split('M')[0]
        intocmoney = int(money_of_club)
        totalint = intocmoney + toadd 
        new_budget = str(totalint)+'M'
        club.budget = new_budget
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
        
        club_money = club_obj.budget.split('M')[0]
        club_money_int = int(club_money)
        player_price = player.price.split('M')[0]
        player_price_int = int(player_price)
        
        if club_money_int < player_price_int:
            return Response('The club does not have enough money to buy the player',status=status.HTTP_401_UNAUTHORIZED)
        else:
            #Adding the player to the club and taking what the club payed for the player
            player.club = club_obj
            player.save()
            club_budget = club_money_int - player_price_int
            new_budget = str(club_budget)+'M'
            club_obj.budget = new_budget
            club_obj.save()
            serializer = PlayerSerializer(player,many=False)
            return Response(serializer.data)
        
#---------------------------
#|   Views for Users       |
#---------------------------      

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CreateUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        user_email = request.data.get('email')
        
        if serializer.is_valid():
            if user_email.split('@')[1] == 'yopmail.com':
                return Response('We do not accept temporary emails', status=status.HTTP_409_CONFLICT)
            else:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShowUsers(APIView):
    def get(self,request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
class Login(APIView):
    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            return Response('No user with that email',status=status.HTTP_404_NOT_FOUND)
        
        if user.password == password:
            serializer = UserSerializer(user,many=False)
            return Response(serializer.data)
        else:
            return Response('Wrong password',status=status.HTTP_401_UNAUTHORIZED)
     
