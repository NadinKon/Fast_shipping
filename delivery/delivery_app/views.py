from rest_framework import viewsets
from .models import Location, Truck, Cargo
from .serializers import LocationSerializer, TruckSerializer, CargoSerializer
from rest_framework.response import Response
from rest_framework import status
from geopy.distance import geodesic


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer

class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer

    def create(self, request, *args, **kwargs):
        pick_up_zip = request.data.get('pick_up_zip')
        delivery_zip = request.data.get('delivery_zip')

        pick_up_location = Location.objects.get(zip=pick_up_zip)
        delivery_location = Location.objects.get(zip=delivery_zip)

        weight = request.data.get('weight')
        description = request.data.get('description')

        truck_id = request.data.get('truck_id')
        if truck_id is not None:
            truck = Truck.objects.get(id=truck_id)
        else:
            truck = None

        cargo = Cargo.objects.create(
            pick_up_location_id=pick_up_location.id,
            delivery_location_id=delivery_location.id,
            weight=weight,
            description=description
        )

        serializer = self.get_serializer(cargo)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = []

        for cargo in queryset:
            cargo_data = self.serializer_class(cargo).data
            nearby_trucks = 0
            cargo_pick_up_location = (cargo.pick_up_location.latitude, cargo.pick_up_location.longitude)

            for truck in Truck.objects.all():
                truck_location = (truck.location.latitude, truck.location.longitude)
                if geodesic(cargo_pick_up_location, truck_location).miles <= 450:
                    nearby_trucks += 1

            cargo_data['nearby_trucks'] = nearby_trucks
            data.append(cargo_data)

        return Response(data)


