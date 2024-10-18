import board
import adafruit_dht
from w1thermsensor import W1ThermSensor, Sensor
import json
import time

roof_sensor = W1ThermSensor(sensor_type=Sensor.DS18B20, sensor_id="3cd2f64802d3")
pool_sensor = W1ThermSensor(sensor_type=Sensor.DS18B20, sensor_id="25780e1e64ff")

dhtDevice = adafruit_dht.DHT22(board.D27, use_pulseio=False)


while True:
    
    pool_temp = pool_sensor.get_temperature()
    roof_temp = roof_sensor.get_temperature()

             
    try:
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
    except RuntimeError:
        pass


    sensor_data = {
        "pool_temp": round(pool_temp, 1),
        "lapa_temp": temperature_c,
        "roof_temp": round(roof_temp, 1),
        "humidity": humidity,
    }

    save_data = json.dumps(sensor_data, indent=4)


    with open("sensor_data.json", "w") as save_file:
        save_file.write(save_data)
        
    time.sleep(3)
