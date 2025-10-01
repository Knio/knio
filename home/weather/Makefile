

define UDEV_RULE
SUBSYSTEMS=="usb", ATTRS{idVendor}=="0bda", ATTRS{idProduct}=="2838", ENV{ID_SOFTWARE_RADIO}="1", MODE="0660", GROUP="plugdev"
endef


weather: install-udev
	python3 weather.py


/etc/udev/rules.d/20-rtl-sdr.rules:
	echo '$(UDEV_RULE)' | sudo tee $@
	sudo udevadm control --reload-rules
	sudo udevadm trigger

install-udev: /etc/udev/rules.d/20-rtl-sdr.rules


.PHONY: install-udev
