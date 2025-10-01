

## Installing a new Debian server


### Add User
Login as admin with private key with kitty:

```sh
sudo nano /etc/hostname zkpq.ca
sudo /sbin/adduser tom
sudo /sbin/usermod -aG sudo tom
```

`visudo`
Add:
```conf
Defaults        timestamp_timeout=1380
```

Login as you:
`su - tom`

### Edit ssh config:

```
sudo nano /etc/ssh/sshd_config
```

```conf
# HostKey /etc/ssh/ssh_host_rsa_key
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

```sh
cd /etc/ssh
sudo rm ssh_host_*key*
sudo ssh-keygen -t ed25519 -f ssh_host_ed25519_key -N "" < /dev/null
# sudo ssh-keygen -t rsa -b 4096 -f ssh_host_rsa_key -N "" < /dev/null
```

Restart sshd

```sh
sudo service ssh restart
```

Check with SSHSec: https://sshsec.zkpq.ca/<IP>

Can now test login from other shell.


## Update OS software

Make swapfile:
```
time sudo dd if=/dev/zero of=/swapfile bs=128M count=32
sudo chmod 0600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
sudo swapon --show
echo '/swapfile swap swap defaults 0 0' | sudo tee -a /etc/fstab
```


## Mount home

`sudo apt install nfs-common cifs-utils`
`sudo nano /etc/fstab`:
```conf
10.87.1.5:/mnt/zp/tom/home /home/tom nfs soft,softreval,timeo=10,nconnect=5,vers=4.2,addr=10.87.1.5,clientaddr=10.87.1.4     0 0
\\10.87.1.5\tom /mnt/zp/tom    cifs username=tom,uid=tom,gid=tom,soft,noperm,noacl    0 0
```

## Install home
```
Generate ssh id:

```sh
ssh-keygen -t ed25519
cat ~/.ssh/id_ed25519.pub
```

Copy to GitHub settings

```sh
sudo apt install git make
git clone git@github.com:Knio/knio

cd knio/config/install
make

logout
```

```sh
apt install weechat --no-install-recommends
```


## Fix Apt
Adds non-free, contrib tags, and backports list
`sudo nano /etc/apt/sources.list`
```
deb http://mirror.it.ubc.ca/debian/ trixie main non-free-firmware contrib non-free
deb-src http://mirror.it.ubc.ca/debian/ trixie main non-free-firmware  contrib non-free

deb http://security.debian.org/debian-security trixie-security main non-free-firmware contrib non-free
deb-src http://security.debian.org/debian-security trixie-security main non-free-firmware contrib non-free

# trixie-updates, to get updates before a point release is made;
# see https://www.debian.org/doc/manuals/debian-reference/ch02.en.html#_updates_and_backports
deb http://mirror.it.ubc.ca/debian/ trixie-updates main non-free-firmware contrib non-free
deb-src http://mirror.it.ubc.ca/debian/ trixie-updates main non-free-firmware contrib non-free

deb http://mirror.it.ubc.ca/debian/ trixie-backports main non-free-firmware contrib non-free
deb-src http://mirror.it.ubc.ca/debian/ trixie-backports main non-free-firmware contrib non-free

```

## AWS Docs Volume
- snapshot existing docs EBS volume
- create new volume
- mount to new instance


### Build VeraCrypt
```
sudo apt install pkg-config libpcsclite-dev libfuse-dev
wget https://github.com/wxWidgets/wxWidgets/releases/download/v3.0.5/wxWidgets-3.0.5.tar.bz2
tar xvf wxWidgets-3.0.5.tar.bz2
make NOGUI=1 WXSTATIC=1 WX_ROOT=$PWD/wxWidgets-3.0.5 wxbuild
make NOGUI=1 WXSTATIC=1
```


Mount docs:
```
cd ~/mnt
make mount.docs
```
