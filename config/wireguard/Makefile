
server_start: server_config
	sudo sysctl -w net.ipv4.ip_forward=1
	sudo iptables -A FORWARD -i wg0 -j ACCEPT
	sudo iptables -A POSTROUTING -o ens5 -j MASQUERADE -t nat
	sudo ip link set up dev wg0


server_interface:
	sudo ip link add dev wg0 type wireguard
	sudo ip address add dev wg0 10.10.0.1/24


server_config: server_interface
	python3 wireguard.py server > wg.conf
	sudo wg setconf wg0 wg.conf
	sudo wg set wg0 private-key privatekey


make_keys:
	wg genkey | tee private.key | wg private.key > public.key
	chmod 600 *.key


listen_inner:
	sudo tcpdump -i wg0


listen_outer:
	sudo tcpdump -i ens5 'port 123'
