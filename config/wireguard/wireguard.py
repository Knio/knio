#!/usr/bin/env python3

'''
Generate wireguard config files.

See: https://www.wireguardconfig.com

'''

SERVER = dict(
  PublicKey = '5r/W9FmLHrJ/HXooBn1/x8yvrqBJaltG2vcYuEWy1T8=',
  Endpoint = 'zkpq.ca:123',
)

SERVER_ONLY = dict(
  Address = '10.10.0.1',
  ListenPort = '123',
  PostUp = 'iptables -A POSTROUTING -o ens5 -j MASQUERADE -t nat',
  PostDown = 'iptables -D POSTROUTING -o ens5 -j MASQUERADE -t nat',
)

CLIENTS = dict(

  desktop = dict(
    PublicKey = 'LejwoIzf8L0/kEkI9/KS8zCdhh4kw7+OtI7srd8YDjo=',
    Address = '10.10.0.2',
  ),

  laptop = dict(
    PublicKey = 'SlDjBmYqSq8hg9st6HkWOzAVVvu//2XLdNjrpu7HHUI=',
    Address = '10.10.0.3',
  ),

  phone = dict(
    PublicKey = 'LZTCbUadB0/sPnw0UBY3SiNbmjwsnDD491pPTGzZ2Vk=',
    Address = '10.10.0.4',
  ),

)

DNS = '1.1.1.1, 4.2.2.1, 8.8.8.8, 9.9.9.9'
MASK = '24'
SUBNET = f'10.10.0.0'


def get_config_for_host(host):
  conf = []
  if host == 'server':
    section = {}
    section |= SERVER
    section |= SERVER_ONLY
    section.pop('Endpoint')
    section.pop('PublicKey')
    section['Address'] += f'/{MASK}'
    conf.append(('Interface', section))

    for name, client in CLIENTS.items():
      section = {}
      section['#Host'] = name
      section |= client
      addr = section.pop('Address')
      section['AllowedIPs'] = f'{addr}/32'
      section['PersistentKeepalive'] = '5'
      conf.append(('Peer', section))
    return conf

  # self
  section = {}
  section['DNS'] = DNS
  section |= CLIENTS[host]
  section.pop('PublicKey')
  section['Address'] += f'/{MASK}'
  conf.append(('Interface', section))

  # server
  section = {}
  section |= SERVER
  section['PersistentKeepalive'] = '5'
  section['AllowedIPs'] = f'{SUBNET}/{MASK}'
  conf.append(('Peer', section))


  return conf



def print_config(config):
  for heading, section in config:
    print(f'[{heading}]')
    for key, value in section.items():
      print(f'{key:<20} = {value}')
    print('')


if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser(argparse.RawTextHelpFormatter, description=__doc__)
  parser.add_argument('host')
  args = parser.parse_args()
  config = get_config_for_host(args.host)
  print_config(config)
