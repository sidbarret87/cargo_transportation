from django.db import models

# Create your models here.

class Location(models.Model):
    city = models.CharField(max_length=255)
    state_id = models.CharField(max_length=255)
    state_name = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    latitude = models.FloatField()
    longitude = models.FloatField()


class Cargo(models.Model): # Груз
    pickup_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='pickups') # локация места погрузки
    delivery_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='deliveries') # локация места доставки
    weight = models.IntegerField()
    description = models.CharField(max_length=255)

class Truck(models.Model): # Машина
    number = models.CharField(max_length=10, unique=True)
    current_location = models.ForeignKey(Location, on_delete= models.CASCADE)
    capacity = models.IntegerField() # грузоподъёмность