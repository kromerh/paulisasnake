# paulisasnake

RPi3 temperature and humidity sensor

## bluetooth on RPi3
https://tutorials-raspberrypi.de/raspberry-pi-3-wlan-einrichten-bluetooth/

## Sensirion latest project
https://github.com/abrauchli/python-smartgadget

## Installation of MongoDB on RPi3 with Python3
- Install the packages with `sudo apt-get install mongodb`

- Create directory `/data/db`, be sure to check permissions correctly with `sudo chrown -R mongodb /data/db/`

- Start mongodb service using `sudo systemctl start mongodb.service`

- Check that it is also running with a restart of the system 

- Install python packages `python3 -m pip install pymongo==3.4.0 pandas numpy`

## MongoDB access and crontab

- the data from the test sensor is stored in the database `sensirion_test`, collection is `temp_and_humid`. 
- to check, connect to the RPi3 and run `mongo`. Then run `use sensirion_test` and find everything in the collection using `db.temp_and_humid.find()`.
- execute `read_sensirion_and_insert_to_mongo.py` every minute in crontab adding `* * * * * python3 /home/pi/paulisasnake/Sensirion_smart_meter/read_sensirion_and_insert_to_mongo.py` to crontab -e

# OLD VERSION

## Hardware

- NodeMCU Lua Lolin V3 Module ESP8266 ESP-12E
- DHT22 sensor
- jumper cables
- power supply
- breadboard(s)

## Tutorial to use the ESP8266 and DHT as well as Watson IoT

https://github.com/binnes/esp8266Workshop
