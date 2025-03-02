
PORT = 7563
BUSID0 = 3-2.5
BUSID1 = 3-2.1

show:
	lsusb -tvvv
	usbip list --local

stop:
	-sudo usbip unbind --busid $(BUSID0)
	-sudo usbip unbind --busid $(BUSID1)
	-sudo kill `cat /var/run/usbipd.pid`

start: stop
	sudo modprobe usbip-host
	sudo usbipd --daemon --tcp-port $(PORT)
	sudo usbip bind --busid $(BUSID0)
	sudo usbip bind --busid $(BUSID1)

.PHONY: start stop

