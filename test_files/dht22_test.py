import board
import adafruit_dht
import time

# Test DHT22 Sensor on Pin 27 Raspberry pi

dhtDevice = adafruit_dht.DHT22(board.D24, use_pulseio=False)

while True:
    try:
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
        print('Temperature: {:.1f} C'.format(temperature_c))
        print('Humidity: {:.1f} %'.format(humidity))

    except RuntimeError:
        print("Failed to get reading")
        #pass

    time.sleep(3)