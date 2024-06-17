SHELL=/bin/bash -o pipefail
HOST = `hostname`
KERNEL_VERSION = $(shell uname -r)

start: /etc/wireguard/wg0_start.sh
	sudo $<


stop: /etc/wireguard/wg0_start.sh
	sudo $< stop


install:
	sudo apt install wireguard
	#sudo apt install python3-bpfcc
	#sudo apt install linux-headers-$(KERNEL_VERSION)
	python3 -m pip install toml

/etc/wireguard:
	sudo mkdir -p /etc/wireguard
	sudo chmod 755 /etc/wireguard

/etc/wireguard/wg0.conf: /etc/wireguard wireguard.py config.toml
	python3 wireguard.py --type conf --host $(HOST) | sudo tee $@
	sudo chmod 600 /etc/wireguard/wg0.conf

/etc/wireguard/wg0_start.sh: /etc/wireguard /etc/wireguard/wg0.conf wireguard.py config.toml
	python3 wireguard.py --type script --host $(HOST) | sudo tee $@
	sudo chmod +x $@

	echo "USER DO: "
	echo "$ sudo crontab -e"
	echo "add:"
	echo "@reboot ${@}"


listen_inner:
	sudo tcpdump -i wg0

listen_outer:
	sudo tcpdump -i ens5 'port 123'


.PHONY: start stop install listen_inner listen_outer
