from django.db import models

# Create your models here.
class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} ({self.code})"

class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures") 
    # related name is basically the reversal. Flight.origin gives the airport of origin of the flight
    # the related name is the flights going out of that origin / that airport
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()


    # basically gives all the information about the flight in a nice clean way
    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"

    # addition at Week 7 for testing lecture
    # make sure this flight is valid by checking these conditions
    def is_valid_flight(self):
        return self.origin != self.destination or self.duration >= 0



# after making edits, use python manage.py makemigrations and then python manage.py migrate
# then run commands with python manage.py shell

# create an object (ex: jfk = Airport(code="JFK", city="London")) and then do jfk.save()


class Passenger(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    flights = models.ManyToManyField(Flight, blank=True, related_name="passengers")

    def __str__(self):
        return f"{self.first} {self.last}"