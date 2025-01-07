from rest_framework import serializers
from .models import RoomTable, RestaurantTable, RentedVehicle, Spot

class RoomTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomTable
        fields = '__all__'

class RestaurantTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantTable
        fields = '__all__'

class RentedVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentedVehicle
        fields = '__all__'

class SpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spot
        fields = '__all__'
