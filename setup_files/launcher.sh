#!/bin/sh


# shellcheck disable=SC2164
cd /home/fanie/Desktop/pool-controller/

sleep 15

python read_sensors.py &

sleep 3

python main.py &

cd /

