from rest_framework import serializers
from .models import Location, Truck, Cargo


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class TruckSerializer(serializers.ModelSerializer):
    current_location = LocationSerializer()

    class Meta:
        model = Truck
        fields = '__all__'


class CargoSerializer(serializers.ModelSerializer):
    pick_up_location = LocationSerializer()
    delivery_location = LocationSerializer()

    class Meta:
        model = Cargo
        fields = '__all__'
