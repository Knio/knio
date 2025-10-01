install:
	python3 -m pip install -r requirements.txt

home:
	python3 home.py

weather:
	python3 weather.py

air:
	# see: bin/ch9344/Makefile
	sudo chmod 666 /dev/ttyCH9344USB0
	python3 air.py /dev/ttyCH9344USB0

co2:
	sudo chmod o+rw /dev/ttyUSB0
	python3 -m devices.arduino_cir_co2 /dev/ttyUSB0

power_meter:
	python3 -m devices.tuya.test

solar:
	python3 solar.py --port /dev/ttyUSB0


socks-service: /etc/systemd/system/socks.service

/etc/systemd/system/socks.service: socks.service
	cat $< | sudo tee $@
	sudo systemctl daemon-reload
	sudo systemctl enable $@
