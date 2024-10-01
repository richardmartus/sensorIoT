from rest_framework import serializers
from .models import SensorData
from rest_framework import generics


class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = ['timestamp', 'voltaje', 'rs', 'calidad_aire']


class SensorDataList(generics.ListCreateAPIView):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer
