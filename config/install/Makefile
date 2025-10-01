REL = $(shell realpath --relative-to ~ ${PWD}/..)
HOME = $(shell echo ~)

all: apt fzf py

ssh:
	cp -R ~/.ssh ~/.ssh.bak
	mv ~/.ssh/* ../dot/.ssh/
	rm -r ~/.ssh
	# link will put it back

link:
	-@for i in `find ~/$(REL)/dot -maxdepth 1 -type f,d -printf '%P\n'`; do \
		F="$(HOME)/$$i"; \
		T="$(REL)/dot/$$i"; \
		echo "$$F -> $$T"; \
		if test -e "$$F"; then echo "    exists, skipping"; continue; fi; \
		ln --backup=t --suffix bak -s "$$T" "$$F"; \
	done
	mkdir -p ~/.config
	-@for i in `find ~/$(REL)/dotconfig -maxdepth 1 -type f,d -printf '%P\n'`; do \
		F="$(HOME)/.config/$$i"; \
		T="../$(REL)/dotconfig/$$i/"; \
		echo "$$F -> $$T"; \
		if test -e "$$F"; then echo "    exists, skipping"; continue; fi; \
		ln --backup=t --suffix bak -s "$$T" "$$F"; \
	done

apt:
	sudo apt update
	sudo apt upgrade
	sudo apt dist-upgrade
	sudo apt autoremove
	sudo apt install \
		git \
		build-essential \
		python3-pip \
		cifs-utils \
		mosh \
		screen \
		zsh \
		curl \
		unattended-upgrades \
		apt-listchanges
	sudo dpkg-reconfigure --priority=low unattended-upgrades


fzf:
	-rm ~/.fzf -rf
	@git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
	@~/.fzf/install


BASHSTR = '[ -f ~/knio/config/bash/bash ] && source ~/knio/config/bash/bash'

bash:
	grep -qxF $(BASHSTR) ~/.bashrc || echo $(BASHSTR) >> ~/.bashrc

py:
	pip install rich
	python3 ../python/usercustomize_install.py


systemd:
	sudo loginctl enable-linger `whoami`
	sudo systemctl --user daemon-reload


host_keys:
	sudo rm -v /etc/ssh/ssh_host_*key*
	sudo ssh-keygen -t ed25519 -f /etc/ssh/ssh_host_ed25519_key -N "" < /dev/null


~/bin/veracrypt-console-%-amd64.deb:
	mkdir -p ~/bin
	wget 'https://launchpad.net/veracrypt/trunk/1.26.14/+download/veracrypt-console-1.26.14-Debian-12-amd64.deb' \
		-O $@

veracrypt: ~/bin/veracrypt-console-1.26.14-Debian-12-amd64.deb
	sudo apt install pcscd
	sudo dpkg -i $<




.PHONY: link ssh fzf bash py veracrypt
