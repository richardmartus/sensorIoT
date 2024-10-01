from django.db import models


class SensorData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    voltaje = models.FloatField()
    rs = models.FloatField()
    calidad_aire = models.CharField(max_length=100)

    def __str__(self):
        return f"Medición {self.timestamp}: {self.calidad_aire}"
