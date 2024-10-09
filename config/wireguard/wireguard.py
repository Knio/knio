#!/usr/bin/env python3

'''
Generate wireguard config files.

See: https://www.wireguardconfig.com

'''

import ipaddress
import pathlib
import subprocess
import toml

CONFIG = toml.load(pathlib.Path(__file__).parent / 'config.toml')
LAN = CONFIG['LAN']
SITE = CONFIG['site']
CLIENT = CONFIG['client']
NW = ipaddress.IPv4Network(LAN['NETWORK'])

# 2600:1f13:07ad:fd01:3daa:0087:0012:0001
#  /16  /32  /48  /64  /80  /96 /112 /128


# TODO: use ipaddress stdlib


def get_pubkey(config):
  if pubkey := config.get('PublicKey'):
    return pubkey
  if privkey := config.get('PrivateKey'):
    return subprocess.check_output(['wg', 'pubkey'], input=privkey, encoding='ascii').strip()
  raise ValueError('no keys')


def get_addr(octet):
  return f'{LAN["PREFIX"]}{octet}'


def get_addr6(octet):
  return f'{LAN["PREFIX6"]}{octet:04d}:0001'


def get_site(host):
  conf = dict(CONFIG['site_defaults']) | SITE[host]
  sn = ipaddress.IPv4Network((
    int(NW.network_address) | (conf['site'] << 8),
    conf['mask']))

  gw = ipaddress.IPv4Interface((int(sn.network_address) | 1, conf['mask']))

  ips = [sn]
  ips += [ipaddress.IPv4Interface(a) for a in conf['allowed']]

  conf |= dict(
    sn = sn,
    gw = gw,
    ips = ips,
    PublicKey = get_pubkey(conf),
  )
  return conf


def get_config_for_site(host):
  conf = get_site(host)
  wg_conf = [(f'[Interface] # {host}', interface := {})]
  interface |= dict(
    PrivateKey = conf['PrivateKey'],
    ListenPort = conf['ListenPort'],
  )
  sn = ipaddress.IPv4Network(int(NW.network_address) | (conf['site'] << 8))

  for name in SITE.keys():
    if name == host: continue
    site = get_site(name)
    wg_conf.append((f'[Peer] # {name}', wg_peer := {}))
    wg_peer |= dict(
      PublicKey = site['PublicKey'],
      AllowedIPs = ', '.join(map(str, site['ips'])),
      PersistentKeepalive = site['PersistentKeepalive'],
      Endpoint = f'{name}:{site["ListenPort"]}'
    )

  for name, client_ in CLIENT.items():
    client = dict(CONFIG['client_defaults'])
    client |= client_
    wg_conf.append((f'[Peer] # {name}', wg_peer := {}))
    ips = ipaddress.IPv4Network(int(sn.network_address) | client['Address'])
    wg_peer |= dict(
      PublicKey = get_pubkey(client),
      AllowedIPs = ips
    )

  return wg_conf


def get_config_for_client(host):
  conf = dict(CONFIG['client_defaults']) | CLIENT[host]
  wg_conf = [(f'[Interface] # {host}', interface := {})]
  pk = conf.get('PrivateKey')
  if pk:
    interface |= dict(PrivateKey=pk)

  interface['DNS'] = ', '.join(LAN['DNS'])

  gw = conf['gateway']
  site = get_site(gw)

  ip = ipaddress.IPv4Interface((
    int(site['sn'].network_address) | conf['Address'],
    LAN['mask']))
  interface['Address'] = ip

  wg_conf.append((f'[Peer] # {gw}', wg_peer := {}))
  wg_peer |= dict(
    PublicKey = site['PublicKey'],
    # AllowedIPs = ', '.join(map(str, site['ips'])),
    AllowedIPs = ipaddress.IPv4Network((0, 0)),
    PersistentKeepalive = site['PersistentKeepalive'],
    Endpoint = f'{gw}:{site["ListenPort"]}'
  )

  return wg_conf


def get_config_for_host(host):
  raise DeprecationWarning
  config = dict(CONFIG['peer_defaults']) | HOSTS[host]

  wg_conf = [('[Interface]', interface := {})]
  interface |= CONFIG['interface_defaults']
  if pk := config.get('PrivateKey'):
    interface['PrivateKey'] = pk
    if lp := config.get('ListenPort'):
      interface['ListenPort'] = lp


  if config.get('is_linux'):
    pass # addresses handled by bash script
  else: # windows
    interface['Address'] = \
        f'{get_addr(config["Address"])}/{LAN["MASK"]}, '
    interface['Address'] += \
        f'{get_addr6(config["Address"])}/{LAN["MASK6"]}'
    interface['DNS'] = ', '.join(LAN['DNS'])


  for name, peer_ in HOSTS.items():
    if name == host:
      continue # self

    peer = dict(CONFIG['peer_defaults'])
    peer |= peer_
    gw = config['gateway']
    px = config['proxy']
    px6 = config['proxy6']
    do = (
      (peer['on_lan'] and config['on_lan']) or
      (name == gw) or
      (name == px) or
      (peer.get('Endpoint')) or
      (config.get('Endpoint'))
    )

    if not do:
      # we won't have a route to them
      continue

    wg_conf.append(('Peer', wg_peer := {}))
    wg_peer['# Host'] = name
    mask = '32'
    mask6 = LAN['PEER6']
    addr = get_addr(peer['Address'])
    addr6 = get_addr6(peer['Address'])
    if (name == gw):
      mask = LAN['MASK']
      mask6 = LAN['MASK6']
    if (name == px):
      mask = '0'
      addr = '0.0.0.0'
    if (name == px6):
      mask6 = '0'
      addr6 = '0::'
    wg_peer |= dict(
      PersistentKeepalive = peer['PersistentKeepalive'],
      PublicKey = get_pubkey(peer),
      # TODO wg doesn't like the masked part the address
      # being :0001, should be :0000
      AllowedIPs =
        f'{addr}/{mask}, '
        f'{addr6}/{mask6}',
    )

    ep = peer.get('Endpoint')
    if not ep and (peer['on_lan'] and config['on_lan']):
      ep = f'{LAN["LAN"]}{peer["Address"]}'
    if ep:
      lp = peer.get('ListenPort', CONFIG['interface_defaults']['ListenPort'])
      wg_peer['Endpoint'] = f'{ep}:{lp}'

  return wg_conf



def get_script_for_site(host):
  conf = get_site(host)

  sn = conf['sn']
  gw = conf['gw']

  wan = conf.get("wan_interface")


# VPC -> Route Tables
# Change the ipv6 subnet from "local" to the server instance
#
# EC2 -> Network interfaces -> Manage prefixes
# IPv6 prefix delegation: Auto-assign


# 06:53:07.032805 IP6 2604:a880:400:d0::1c4d:e001 > 2600:1f13:7ad:fd01:3daa:87:0:9: ICMP6, echo request, id 22867, seq 1, length 64
# 06:53:07.360278 IP6 zkpq.ca > ff02::1:ff00:9: ICMP6, neighbor solicitation, who has 2600:1f13:7ad:fd01:3daa:87:0:9, length 32
# 06:53:07.360326 IP6 2600:1f13:7ad:fd01:3daa:87:0:9 > zkpq.ca: ICMP6, neighbor advertisement, tgt is 2600:1f13:7ad:fd01:3daa:87:0:9, length 32

  script = f'''#!/bin/bash

# autogenerated up script for {host}

set -e
set -u
set -o pipefail
set -x


# clean up everything
ip link set down dev wg0 || true
ip link del dev wg0 || true
iptables -D FORWARD -i wg0 -j ACCEPT || true
iptables -D POSTROUTING -o '{wan}' -j MASQUERADE -t nat || true

if [ $# -eq 1 ] && [ "$1" = "stop" ];
then
  exit
fi

# done cleanup


# set up interface
ip link add dev wg0 type wireguard
wg setconf wg0 /etc/wireguard/wg0.conf
ip address add dev wg0 '{gw}'
# ip address add dev wg0 <<addr6>>
ip link set up dev wg0
'''

  for name in SITE.keys():
    if name == host: continue
    site = get_site(name)
    for ip in site['ips']:
      script += f'''
# route to {name}
ip route add '{ip}' dev wg0 via '{gw.ip}' '''

  script += f'''

echo 1 | tee /proc/sys/net/ipv4/conf/{wan}/proxy_arp

sysctl -w net.ipv4.ip_forward=1
iptables -A FORWARD -i wg0 -j ACCEPT
iptables -A POSTROUTING -o '{wan}' -j MASQUERADE -t nat

# sysctl -w net.ipv6.conf.all.forwarding=1
'''
  return script

def print_config(config):
  for heading, section in config:
    print(heading)
    for key, value in section.items():
      print(f'{key:<20} = {value}')
    print('')


def main(args):
  if args.list_hosts:
    print('\n'.join(SITE.keys() | CLIENT.keys()))
    return
  elif args.type == 'conf':
    h = args.host
    if h in SITE:
      config = get_config_for_site(h)
    elif h in CLIENT:
      config = get_config_for_client(h)
    else:
      raise ValueError(f'no host {h}')
    print_config(config)
    return
  elif args.type == 'script':
    script = get_script_for_site(args.host)
    print(script)
    return
  raise ValueError(f'unknown type {args.type}')


if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser(argparse.RawTextHelpFormatter, description=__doc__)
  parser.add_argument('--list-hosts', action='store_true')
  parser.add_argument('host', nargs='?')
  parser.add_argument('--type', default='conf')
  main(parser.parse_args())
