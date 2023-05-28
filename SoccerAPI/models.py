from django.db import models

# Create your models here.

# Creating the class League, so there is a league for a club. 
# If the Player is an Icon, the name of the League would be Icons and the nation World Wide
class League(models.Model):
    name = models.CharField(max_length=30)
    nation = models.CharField(max_length=30)

    def __str__(self):
        return self.name


# Creating the class Club, the club is inside a League and there will be Club associated with a Player
# A Club will have a budget so if they want to buy a player, they will be able to buy it if the price is
# lower than the budget the club has. 
class Club(models.Model):
    name = models.CharField(max_length=30)
    budget = models.CharField(max_length=5)
    league = models.ForeignKey(League, on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.name

# Creating the class Player, the player must be inside a club
class Player(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    nationallity = models.CharField(max_length=30)
    rating = models.IntegerField()
    price = models.CharField(max_length=5)
    club = models.ForeignKey(Club, on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.name

#Creating the class User
class User(models.Model):
    user_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.user_name
    