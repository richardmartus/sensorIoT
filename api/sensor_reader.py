# sensores/sensor_reader.py

import time
import board
import busio
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn
from .models import SensorData

# Inicializa I2C y ADS1115
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS1115(i2c)

# Parámetros del sensor
RL = 10_000  # Resistencia de carga en ohmios
R0 = 9_830  # Resistencia en aire limpio (esto lo calibras)


# Función para calcular RS
def calcular_rs(voltage, vcc=5.0, rl=RL):
    return (vcc - voltage) / voltage * rl


# Función para estimar la calidad del aire según RS/R0
def estimar_calidad_aire(rs, r0=R0):
    ratio = rs / r0
    if ratio < 1:
        return "Aire limpio (<400 ppm)"
    elif 1 <= ratio < 2:
        return "Aceptable (400 - 1000 ppm)"
    elif 2 <= ratio < 3:
        return "Regular (1000 - 2000 ppm)"
    elif 3 <= ratio < 4:
        return "Malo (2000 - 5000 ppm)"
    else:
        return "Muy malo (>5000 ppm)"


# Leer el valor del canal A0 del ADS1115
canal = AnalogIn(ads, ADS1115.P0)

while True:
    voltaje = canal.voltage
    rs = calcular_rs(voltaje)
    calidad_aire = estimar_calidad_aire(rs)

    # Guardar los valores en la base de datos
    SensorData.objects.create(voltaje=voltaje, rs=rs, calidad_aire=calidad_aire)

    time.sleep(60)  # Medir cada minuto
