import board
import adafruit_dht
from w1thermsensor import W1ThermSensor, Sensor
import json
import time
import requests

#roof_sensor = W1ThermSensor(sensor_type=Sensor.DS18B20, sensor_id="3cd2f64802d3")
pool_sensor = W1ThermSensor(sensor_type=Sensor.DS18B20, sensor_id="25780e1e64ff")

dhtDevice = adafruit_dht.DHT22(board.D27, use_pulseio=False)


while True:


    # -------------------------------------------------------------
    # Get Current Weather Temp from Open Weather API
    # -------------------------------------------------------------
    with open("api.txt", "r") as f:
        api_key = f.read()

    owm_api = "https://api.openweathermap.org/data/2.5/weather"

    weather_params = {
        "lat": -26.585360,
        "lon": 28.006899,
        "units": "metric",
        "appid": api_key
    }

    response = requests.get(owm_api, params=weather_params)

    weather_temp = response.json()["main"]["temp"]




    # -------------------------------------------------------------
    # Get Temp Data from DS18B20 Tempsensor
    # -------------------------------------------------------------
    pool_temp = pool_sensor.get_temperature()
    #roof_temp = roof_sensor.get_temperature()


    # -------------------------------------------------------------
    # Get Temp and Humid Data from DHT22 Sensor
    # -------------------------------------------------------------
    try:
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
    except RuntimeError:
        pass



    # -------------------------------------------------------------
    # Save Data to the sensor_data.json file
    # -------------------------------------------------------------
    sensor_data = {
        "pool_temp": round(pool_temp, 1),
        "lapa_temp": temperature_c,
        "open_temp": round(weather_temp, 1),
        "humidity": humidity,
    }

    save_data = json.dumps(sensor_data, indent=4)


    with open("sensor_data.json", "w") as save_file:
        save_file.write(save_data)
        
    time.sleep(3)
