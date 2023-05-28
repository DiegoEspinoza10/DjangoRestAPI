"""
URL configuration for DjangoRestAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from SoccerAPI.views import ShowLeagues,AddLeagues,AddClub,ShowClubs,ShowClubsByLeague,MoreMoney4Club,SpecificClub,AddPlayer, ShowPlayers, getByNationality, getByClub, TransferPlayer, CreateUser, ShowUsers,Login
urlpatterns = [
    #------------League URLS------------
    path('league/list/',ShowLeagues.as_view()),
    path('addleague/',AddLeagues.as_view()),
    #-------------Club URLS-------------
    path('addclub/',AddClub.as_view()),
    path('clubs/list/',ShowClubs.as_view()),
    path('clubsxleague/<str:league>',ShowClubsByLeague.as_view()),
    path('addmoney/<str:name>',MoreMoney4Club.as_view()),
    path('searchclub/<str:name>',SpecificClub.as_view()),
    #------------Players URLS------------
    path('addplayer/',AddPlayer.as_view()),
    path('player/list/', ShowPlayers.as_view()),
    path('playerxnation/<str:nation>',getByNationality.as_view()),
    path('playerxclub/<str:club>',getByClub.as_view()),
    path('transfer/',TransferPlayer.as_view()), 
    #------------Users URLS------------
    path('adduser/',CreateUser.as_view()),
    path('users/list/',ShowUsers.as_view()),
    path('login/',Login.as_view()),
]