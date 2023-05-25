from django.db import models


class Location(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=6)
    latitude = models.FloatField()
    longitude = models.FloatField()


class Truck(models.Model):
    unique_number = models.CharField(max_length=6)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    load_capacity = models.IntegerField()


class Cargo(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name='cargos', null=True)
    pick_up_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='pick_up_cargos')
    delivery_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='delivery_cargos')
    weight = models.IntegerField()
    description = models.TextField()

