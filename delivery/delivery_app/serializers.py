from rest_framework import serializers
from .models import Location, Truck, Cargo
from geopy.distance import distance


# Serializer для модели Location
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


# Serializer для модели Truck
class TruckSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = Truck
        fields = '__all__'


# Serializer для модели Cargo
class CargoSerializer(serializers.ModelSerializer):
    pick_up_location = LocationSerializer()
    delivery_location = LocationSerializer()

    class Meta:
        model = Cargo
        fields = '__all__'


# Serializer для модели Cargo с дополнительной информацией о расстояниях до грузовиков
class CargoDetailedSerializer(serializers.ModelSerializer):
    pick_up_location = LocationSerializer()  # Для поля pick_up_location используем LocationSerializer
    delivery_location = LocationSerializer()  # Для поля delivery_location используем LocationSerializer
    trucks_distances = serializers.SerializerMethodField()  # Добавляем поле trucks_distances

    class Meta:
        model = Cargo
        fields = ['id', 'pick_up_location', 'delivery_location', 'weight', 'description', 'trucks_distances']

    # Функция для получения списка расстояний от всех грузовиков до данного груза
    def get_trucks_distances(self, obj):
        trucks_distances = []  # Создаем пустой список для хранения результатов
        for truck in Truck.objects.all():  # Проходим по всем грузовикам
            # Рассчитываем расстояние от грузовика до груза
            d = distance(
                (truck.location.latitude, truck.location.longitude),  # Координаты грузовика
                (obj.pick_up_location.latitude, obj.pick_up_location.longitude)  # Координаты груза
            )
            # Добавляем в список пару вида {unique_number: расстояние}
            trucks_distances.append({truck.unique_number: d.miles})
        return trucks_distances  # Возвращаем полученный список
