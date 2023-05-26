from rest_framework import viewsets
from .models import Location, Truck, Cargo
from .serializers import LocationSerializer, TruckSerializer, CargoSerializer, CargoDetailedSerializer
from rest_framework.response import Response
from rest_framework import status
from geopy.distance import geodesic


# ViewSet для модели Location
class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()  # Берем все объекты модели Location
    serializer_class = LocationSerializer  # Используем LocationSerializer для сериализации и десериализации


# ViewSet для модели Truck
class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.all()  # Берем все объекты модели Truck
    serializer_class = TruckSerializer  # Используем TruckSerializer для сериализации и десериализации

    # Переопределяем метод update для изменения локации грузовика по ZIP коду
    def update(self, request, *args, **kwargs):
        zip_code = request.data.get('zip')  # Извлекаем новый ZIP код из запроса
        location = Location.objects.get(zip=zip_code)  # Получаем новую локацию по ZIP коду

        truck = self.get_object()  # Получаем объект грузовика, который нужно обновить
        truck.location = location  # Изменяем его локацию
        truck.save()  # Сохраняем изменения

        serializer = self.get_serializer(truck)  # Сериализуем обновленный объект грузовика
        return Response(serializer.data, status=status.HTTP_200_OK)  # Возвращаем сериализованные данные с успешным статусом


# ViewSet для модели Cargo
class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()  # Берем все объекты модели Cargo
    serializer_class = CargoSerializer  # Используем CargoSerializer для сериализации и десериализации

    # Переопределяем метод create для создания нового груза
    def create(self, request, *args, **kwargs):
        pick_up_zip = request.data.get('pick_up_zip')  # Извлекаем ZIP код места погрузки из запроса
        delivery_zip = request.data.get('delivery_zip')  # Извлекаем ZIP код места доставки из запроса

        # Получаем места погрузки и доставки по их ZIP кодам
        pick_up_location = Location.objects.get(zip=pick_up_zip)
        delivery_location = Location.objects.get(zip=delivery_zip)

        weight = request.data.get('weight')  # Извлекаем вес груза из запроса
        description = request.data.get('description')  # Извлекаем описание груза из запроса

        truck_id = request.data.get('truck_id')  # Извлекаем ID грузовика из запроса
        if truck_id is not None:  # Если ID грузовика указан,
            truck = Truck.objects.get(id=truck_id)  # то получаем этот объект грузовика,
        else:
            truck = None  # иначе оставляем значение None

        # Создаем новый объект груза
        cargo = Cargo.objects.create(
            pick_up_location_id=pick_up_location.id,
            delivery_location_id=delivery_location.id,
            weight=weight,
            description=description
        )

        serializer = self.get_serializer(cargo)  # Сериализуем новый объект груза
        return Response(serializer.data, status=status.HTTP_201_CREATED)  # Возвращаем сериализованные данные с успешным статусом

    # Переопределяем метод list для подсчета количества грузовиков, находящихся в радиусе 450 миль от груза
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())  # Фильтруем объекты грузов
        data = []  # Создаем пустой список для хранения данных

        for cargo in queryset:  # Проходим по всем грузам
            cargo_data = self.serializer_class(cargo).data  # Сериализуем данные груза
            nearby_trucks = 0  # Задаем начальное количество грузовиков рядом
            cargo_pick_up_location = (cargo.pick_up_location.latitude, cargo.pick_up_location.longitude)  # Получаем координаты места погрузки груза

            for truck in Truck.objects.all():  # Проходим по всем грузовикам
                truck_location = (truck.location.latitude, truck.location.longitude)  # Получаем координаты грузовика
                # Если грузовик находится в радиусе 450 миль от места погрузки груза,
                if geodesic(cargo_pick_up_location, truck_location).miles <= 450:
                    nearby_trucks += 1  # то увеличиваем счетчик

            cargo_data['nearby_trucks'] = nearby_trucks  # Добавляем количество рядом находящихся грузовиков в данные груза
            data.append(cargo_data)  # Добавляем данные груза в общий список

        return Response(data)  # Возвращаем полученные данные

    # Переопределяем метод retrieve для использования более подробного сериализатора
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()  # Получаем объект груза, который нужно отобразить
        serializer = CargoDetailedSerializer(instance)  # Сериализуем объект с использованием CargoDetailedSerializer
        return Response(serializer.data)  # Возвращаем сериализованные данные

    # Переопределяем метод update для обновления веса и описания груза
    def update(self, request, *args, **kwargs):
        weight = request.data.get('weight')  # Извлекаем новый вес из запроса
        description = request.data.get('description')  # Извлекаем новое описание из запроса

        cargo = self.get_object()  # Получаем объект груза, который нужно обновить
        if weight is not None:  # Если указан новый вес,
            cargo.weight = weight  # то обновляем вес груза
        if description is not None:  # Если указано новое описание,
            cargo.description = description  # то обновляем описание груза
        cargo.save()  # Сохраняем изменения

        serializer = self.get_serializer(cargo)  # Сериализуем обновленный объект груза
        return Response(serializer.data, status=status.HTTP_200_OK)  # Возвращаем сериализованные данные с успешным статусом
