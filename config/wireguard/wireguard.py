#!/usr/bin/env python3

'''
Generate wireguard config files.

See: https://www.wireguardconfig.com

'''

DNS = '1.1.1.1, 4.2.2.1, 8.8.8.8, 9.9.9.9'
MASK = '24'
SUBPRE = '10.87.0.'
SUBNET = f'{SUBPRE}0'


SERVER = dict(
  PublicKey = '5r/W9FmLHrJ/HXooBn1/x8yvrqBJaltG2vcYuEWy1T8=',
  Endpoint = 'zkpq.ca:123',
)

SERVER_ONLY = dict(
  Address = '1',
  ListenPort = '123',
  PostUp = 'iptables -A POSTROUTING -o ens5 -j MASQUERADE -t nat',
  PostDown = 'iptables -D POSTROUTING -o ens5 -j MASQUERADE -t nat',
)

CLIENTS = dict(

  desktop = dict(
    PublicKey = 'LejwoIzf8L0/kEkI9/KS8zCdhh4kw7+OtI7srd8YDjo=',
    Address = '10',
  ),

  laptop = dict(
    PublicKey = 'YwQ1qRu9tWBmz4d+oYL7u9PlZqEt11u6j+Drrjt2yWY=',
    Address = '12',
  ),

  phone = dict(
    PublicKey = 'LZTCbUadB0/sPnw0UBY3SiNbmjwsnDD491pPTGzZ2Vk=',
    Address = '15',
  ),

  rpizw = dict(
    PublicKey = 'ERYHFwoPJkWRm3PSZMDxaZUJCsxuh5z/M4kL8njyyQc=',
    Address = '17',
  ),
  lab_sp6 = dict(
    PublicKey = 'XMG1tDSl63J69uW1/I/UPXlxJt/tJuptPDHFFBtzojE=',
    Address = '18',
  ),



)


def get_config_for_host(host):
  conf = []
  if host == 'server':
    section = {}
    section |= SERVER
    section |= SERVER_ONLY
    section.pop('Endpoint')
    section.pop('PublicKey')
    section['Address'] += f'/{MASK}'

    # TODO not supported on old wg?
    section.pop('Address')
    section.pop('PostUp')
    section.pop('PostDown')

    conf.append(('Interface', section))

    for name, client in CLIENTS.items():
      section = {}
      section['#Host'] = name
      section |= client
      addr = section.pop('Address')
      section['AllowedIPs'] = f'{SUBPRE}{addr}/32'
      section['PersistentKeepalive'] = '5'
      conf.append(('Peer', section))
    return conf

  # self
  section = {}
  section['DNS'] = DNS
  section |= CLIENTS[host]
  section.pop('PublicKey')
  addr = section['Address']
  section['Address'] = f'{SUBPRE}{addr}/{MASK}'
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
