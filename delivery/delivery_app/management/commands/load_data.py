import csv
import random
import string

from django.core.management.base import BaseCommand
from geopy.distance import distance
from geopy.distance import geodesic
from delivery_app.models import Location, Truck



class Command(BaseCommand):
    help = 'Load locations from CSV and create trucks'

    def handle(self, *args, **options):
        with open('C:\\Users\\Nadin\PycharmProjects\Fast_shipping\delivery\delivery_app\\uszips.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                location = Location.objects.create(
                    zip=row['zip'],
                    latitude=row['lat'],
                    longitude=row['lng'],
                    city=row['city'],
                    state=row['state_id']
                )
        for i in range(1, 21):
            location = random.choice(Location.objects.all())
            unique_number = f'{random.randint(1000, 9999)}{random.choice(string.ascii_uppercase)}'
            load_capacity = random.randint(1, 1000)
            Truck.objects.create(
                unique_number=unique_number,
                location=location,
                load_capacity=load_capacity
            )
        for truck in Truck.objects.all():
            for cargo in truck.cargos.all():
                d = geodesic(
                    (truck.location.latitude, truck.location.longitude),
                    (cargo.pick_up_location.latitude, cargo.pick_up_location.longitude)
                )
                print(f'The distance from truck {truck.unique_number} to cargo {cargo.id} is {d.miles} miles.')
