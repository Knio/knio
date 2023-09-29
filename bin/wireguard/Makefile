
server_start: server_config
	sudo sysctl -w net.ipv4.ip_forward=1
	sudo iptables -A POSTROUTING -o ens5 -j MASQUERADE -t nat
	sudo ip link set up dev wg0


server_interface:
	sudo ip link add dev wg0 type wireguard
	sudo ip address add dev wg0 192.168.2.1/24


server_config: server_interface phone_client
	sudo wg set wg0 listen-port 123
	sudo wg set wg0 private-key ~.config/wireguard/privatekey


phone_client:
	sudo wg set wg0 \
		peer 'LZTCbUadB0/sPnw0UBY3SiNbmjwsnDD491pPTGzZ2Vk=' \
		allowed-ips 192.168.2.2/32 \
		persistent-keepalive 1


make_keys:
	wg genkey | tee privatekey | wg pubkey > publickey
	chmod 600 *key


listen_inner:
	sudo tcpdump -i wg0


listen_outer:
	sudo tcpdump -i ens5 'port 123'
