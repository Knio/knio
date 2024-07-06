install:
	python3 -m pip install -r requirements.txt

start_all: \
		start_home \
		start_air \
		start_weather \
		start_co2


start_home:
	python home.py

start_weather:
	python weather.py

start_air:
	-sh -c 'cd ~/bin/ch9344ser_linux/driver; sudo make load'
	python air.py /dev/ttyCH9344USB0

start_co2:
	python -m devices.arduino_cir_co2 /dev/ttyUSB0
