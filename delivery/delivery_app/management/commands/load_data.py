import csv
import random
import string
from django.core.management.base import BaseCommand
from geopy.distance import geodesic
from delivery_app.models import Location, Truck


class Command(BaseCommand):
    help = 'Load locations from CSV and create trucks'

    def handle(self, *args, **options):
        # Открываем файл CSV
        with open('/app/uszips.csv', newline='') as f:
            reader = csv.DictReader(f)  # Читаем CSV-файл
            for row in reader:  # Проходим по каждой строке
                # Создаем объект Location с данными из строки
                location = Location.objects.create(
                    zip=row['zip'],
                    latitude=row['lat'],
                    longitude=row['lng'],
                    city=row['city'],
                    state=row['state_id']
                )
        # Создаем 20 объектов Truck
        for i in range(1, 21):
            # Выбираем случайный объект Location из всех существующих
            location = random.choice(Location.objects.all())
            # Генерируем уникальный номер для грузовика
            unique_number = f'{random.randint(1000, 9999)}{random.choice(string.ascii_uppercase)}'
            # Генерируем грузоподъемность для грузовика
            load_capacity = random.randint(1, 1000)
            # Создаем объект Truck с сгенерированными данными и выбранным объектом Location
            Truck.objects.create(
                unique_number=unique_number,
                location=location,
                load_capacity=load_capacity
            )
        # Проходим по каждому объекту Truck
        for truck in Truck.objects.all():
            # Проходим по каждому грузу, привязанному к текущему грузовику
            for cargo in truck.cargos.all():
                # Вычисляем расстояние от грузовика до места погрузки груза
                d = geodesic(
                    (truck.location.latitude, truck.location.longitude),
                    (cargo.pick_up_location.latitude, cargo.pick_up_location.longitude)
                )
                # Выводим информацию о расстоянии от грузовика до места погрузки груза
                print(f'The distance from truck {truck.unique_number} to cargo {cargo.id} is {d.miles} miles.')
