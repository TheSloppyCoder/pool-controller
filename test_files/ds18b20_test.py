import time
from w1thermsensor import W1ThermSensor, Sensor


# Sensors are connected to GPIO Pin 4 on Raspberry pi

# Test with Only 1 Sensor regardless the sensor address
# sensor = W1ThermSensor()
# while True:
#     temperature = sensor.get_temperature()
#     print("Temp: " ,temperature)
#     time.sleep(1)

#################################################################################
#################################################################################


# Test with multiple Sensors or per Sensor Address
sensor1 = W1ThermSensor(sensor_type=Sensor.DS18B20, sensor_id="3cd2f64802d3")
sensor2 = W1ThermSensor(sensor_type=Sensor.DS18B20, sensor_id="25780e1e64ff")

while True:
    temperature1 = sensor1.get_temperature()
    temperature2 = sensor2.get_temperature()

    print(temperature1)
    print(temperature2)
    time.sleep(1)


