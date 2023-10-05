from geopy.distance import geodesic
from rest_framework import generics, status
from rest_framework.response import Response

from cargos.models import Cargo, Location
from cargos.serializers import CargoSerializer


class CargoCreateView(generics.CreateAPIView):
    queryset = Cargo.objects.all # Здесь устанавливается запрос к базе данных для выбора всех существующих грузов.
    serializer_class = CargoSerializer
    def create(self, request, *args, **kwargs):
        pickup_zip = request.data.get('pickup_zip')
        delivery_zip = request.data.get('delivery_zip')

        pickup_location = Location.objects.filter(zip_code=pickup_zip).first()
        delivery_location = Location.objects.filter(zip_code=delivery_zip).first()

        # Проверка наличия местоположений:
        if not (pickup_location and delivery_location):
            return Response({'Ошибка': 'неверный индекс.' }, status=status.HTTP_400_BAD_REQUEST)

        # Вычисление расстояния между местами

        distance = geodesic(

            (pickup_location.latitude, pickup_location.longitude),
            (delivery_location.latitude, delivery_location.longitude)
        ).miles

        # Подготовка данных о грузе:
        
        cargo_data = {
            'pickup_location': pickup_location.id,
            'delivery_location': delivery_location.id,
            'weight': request.data.get('weight'),
            'description': request.data.get('description')
        }

        # Создание и валидация сериализатора

        serialier = self.get_serializer(data = cargo_data)
        serialier.is_valid(raise_exception=True)

        # Сохранение данных о грузе

        self.perform_create(serialier)
        return Response({'Расстояние': distance}, status=status.HTTP_201_CREATED)

    #В конечном итоге, возвращается ответ с расстоянием между местами отправления и
    #доставки и кодом статуса 201(создано).