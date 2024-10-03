import time
import board
import busio
import mysql.connector
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS1115(i2c)

RL = 10_000
R0 = 9_830


def calcular_rs(voltage, vcc=5.0, rl=RL):
    return (vcc - voltage) / voltage * rl


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


conn = mysql.connector.connect(
    host="179.27.99.160",
    user="remote",
    password="Canelones1119.AID",
    database="sensor"
)

cursor = conn.cursor()

canal = AnalogIn(ads, ADS1115.P0)

while True:
    voltaje = canal.voltage
    rs = calcular_rs(voltaje)
    calidad_aire = estimar_calidad_aire(rs)

    cursor.execute('''
        INSERT INTO api_sensordata (timestamp, voltaje, rs, calidad_aire)
        VALUES (NOW(), %s, %s, %s)
    ''', (voltaje, rs, calidad_aire))

    conn.commit()

    print(f"Datos guardados: Voltaje={voltaje}, RS={rs}, Calidad del Aire={calidad_aire}")

    time.sleep(60)
