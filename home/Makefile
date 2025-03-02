install:
	python3 -m pip install -r requirements.txt

home:
	python3 home.py

weather:
	python3 weather.py

air:
	-sh -c 'cd ~/bin/ch9344ser_linux/driver; sudo make load'
	python3 air.py /dev/ttyCH9344USB0

co2:
	python3 -m devices.arduino_cir_co2 /dev/ttyUSB1

solar:
	python3 solar.py --port /dev/ttyUSB0


socks-service: /etc/systemd/system/socks.service

/etc/systemd/system/socks.service: socks.service
	cat $< | sudo tee $@
	sudo systemctl daemon-reload
	sudo systemctl enable $@
