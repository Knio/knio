
server_start: server_config
	sudo sysctl -w net.ipv4.ip_forward=1
	sudo iptables -A FORWARD -i wg0 -j ACCEPT
	sudo iptables -A POSTROUTING -o ens5 -j MASQUERADE -t nat
	sudo ip link set up dev wg0

server_stop:
	sudo iptables -D FORWARD -i wg0 -j ACCEPT
	sudo iptables -D POSTROUTING -o ens5 -j MASQUERADE -t nat
	sudo ip link set down dev wg0

server_interface:
	sudo ip link add dev wg0 type wireguard
	sudo ip address add dev wg0 10.99.0.1/24

server_config: wg.conf
	sudo wg setconf wg0 wg.conf
	sudo wg set wg0 private-key private.key

wg.conf: wireguard.py
	python3 wireguard.py server > $@

private.key:
	wg genkey > $@
	chmod 600 *.key

public.key: private.key
	sudo wg pubkey < private.key > $@

listen_inner:
	sudo tcpdump -i wg0


listen_outer:
	sudo tcpdump -i ens5 'port 123'

.PHONY: server_start server_stop server_interface server_config listen_inner listen_outer
