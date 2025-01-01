SHELL=/bin/bash -x -o pipefail
HOST ?= `hostname`

update: ini start

start: /etc/wireguard/wg0_start.sh
	sudo $<

stop: /etc/wireguard/wg0_start.sh
	sudo $< stop

install:
	sudo apt install net-tools wireguard-tools iptables tcpdump
	python3 -m pip install toml qrcode

/etc/wireguard:
	sudo mkdir -p /etc/wireguard
	sudo chmod 755 /etc/wireguard

/etc/wireguard/wg0.conf: /etc/wireguard wireguard.py config.toml
	python3 wireguard.py --type conf $(HOST) | sudo tee $@
	sudo chmod 600 /etc/wireguard/wg0.conf

/etc/wireguard/wg0_start.sh: /etc/wireguard /etc/wireguard/wg0.conf wireguard.py config.toml /etc/systemd/system/wg0.service
	python3 wireguard.py --type script $(HOST) | sudo tee $@
	sudo chmod +x $@

/etc/systemd/system/wg0.service: wg0.service
	cat $< | sudo tee $@
	sudo systemctl daemon-reload
	sudo systemctl enable $@


listen_inner:
	sudo tcpdump -i wg0


listen_outer:
	sudo tcpdump -i ens5 'port 8443'


ini: $(shell python3 wireguard.py --list-clients)

$(shell python3 wireguard.py --list-clients): wireguard.py config.toml
	-python3 wireguard.py $@ > host.$@.conf

debug:
	sudo wg
	sudo iptables -L -v -n
	ip route


.PHONY: start stop install listen_inner listen_outer ini
