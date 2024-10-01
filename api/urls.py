from django.urls import path
from .views import SensorDataList

urlpatterns = [
    path('', SensorDataList.as_view(), name='sensor_data_list'),
]
