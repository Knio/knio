# RPi Zero Home Server

```sh
ssh-keygen -t ed25519
cat ~/.ssh/id_ed25519.pub
```
Add key to Github

```sh

sudo apt update
sudo apt upgrade


sudo apt install git python3-dev python3-pip

git clone git@github.com:Knio/knio.git

```

## UART 8ch driver:

Source: https://github.com/WCHSoftGroup/ch9344ser_linux


from `bin/ch9344ser_linux/driver`:

```sh
make
sudo make load
```


