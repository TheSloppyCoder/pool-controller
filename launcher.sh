#!/bin/sh

sleep 10

cd /home/fanie/Desktop/pool-controller/
python read_sensors.py &

sleep 3

python main.py &
cd /

