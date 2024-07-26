install:
	python3 -m pip install -r requirements.txt


home:
	python home.py

weather:
	python weather.py

air:
	-sh -c 'cd ~/bin/ch9344ser_linux/driver; sudo make load'
	python air.py /dev/ttyCH9344USB0

co2:
	python -m devices.arduino_cir_co2 /dev/ttyUSB0

power:
	python power.py

.PHONY: install home weather air co2 power
