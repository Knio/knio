

## Installing a new Debian server


### Add User
Login as admin with private key with kitty:
```
sudo hostname zkpq.ca
sudo /sbin/adduser tom
sudo /sbin/usermod -aG sudo tom
```

Login as you:
`su - tom`

### Edit ssh config:

`nano /etd/ssh/sshd_config`
```
HostKey /etc/ssh/ssh_host_rsa_key
#HostKey /etc/ssh/ssh_host_ecdsa_key
HostKey /etc/ssh/ssh_host_ed25519_key

# Ciphers
KexAlgorithms curve25519-sha256@libssh.org,diffie-hellman-group-exchange-sha256
Ciphers chacha20-poly1305@openssh.com,aes256-ctr,aes192-ctr
MACs hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,umac-128@openssh.com,hmac-sha2-256,hmac-sha2-512


# Logging
SyslogFacility AUTH
LogLevel DEBUG

# Authentication:
LoginGraceTime 2m
PermitRootLogin prohibit-password
StrictModes yes
PasswordAuthentication yes
```

Regenerate host keys
```
cd /etc/ssh
sudo rm ssh_host_*key*
sudo ssh-keygen -t ed25519 -f ssh_host_ed25519_key -N "" < /dev/null
sudo ssh-keygen -t rsa -b 4096 -f ssh_host_rsa_key -N "" < /dev/null
```

Restart sshd
`sudo service ssh restart`

Check with SSHSec: https://sshsec.zkpq.ca/<IP>

Can now login from other shell.
```
ssh-copy-id <IP>
ssh <IP>
```

## Update user software

Generate ssh id:
`ssh-keygen -t rsa 8192`
`cat ~/.ssh/id_rsa.pub`
Copy to GitHub settings


```
sudo apt update
sudo apt upgrade
sudo apt dist-upgrade
sudo apt autoremove

sudo apt install git
git clone git@github.com:Knio/home
mv home/* .
mv home/.* .
rm home -r
echo 'source "$HOME/.bash"' >> .profile
logout
```

```
apt install weechat --no-install-recommends
```
