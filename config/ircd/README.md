

# Install IRCd

```sh
sudo /sbin/adduser ircd
sudo /sbin/usermod -aG www-data ircd
sudo su - ircd
# get latest version from https://www.unrealircd.org/download/
wget https://www.unrealircd.org/downloads/unrealircd-6.B.C.D.tar.gz
tar xvf *.gz
cd unreal<T>
./Config
make
make install
```

Copy config files:
(as `tom`)
```sh
cd ~/Docs/Programming/ircd
sudo cp -R . /home/ircd/unrealircd/conf
sudo chown ircd:ircd /home/ircd/unrealircd/conf -R
```


Start server:
(as `ircd`)
```sh

cd unrealircd/conf/tls
ln -s /etc/letsencrypt/live/zkpq.ca/cert.pem     server.cert.pem
ln -s /etc/letsencrypt/live/zkpq.ca/privkey.pem  server.key.pem

cd ../..

unrealircd/unrealircd start
```
