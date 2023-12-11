ADDR = 10.87.0.1/24
HOST = `hostname`

start: /etc/wireguard/wg0_start.sh
	sudo $<

stop:
	-sudo iptables -D FORWARD -i wg0 -j ACCEPT
	-sudo iptables -D POSTROUTING -o ens5 -j MASQUERADE -t nat
	-sudo ip link set down dev wg0
	-sudo ip link del dev wg0
	-sudo rm -r /etc/wireguard

install:
	sudo apt install wireguard

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
