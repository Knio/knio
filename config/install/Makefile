REL = $(shell realpath --relative-to ~ ${PWD}/..)
HOME = $(shell echo ~)

all: ssh link bash apt fzf

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
		fzf \



fzf:
	-rm ~/.fzf -rf
	@git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
	@~/.fzf/install


BASHSTR = '[ -f ~/knio/config/bash/bash ] && source ~/knio/config/bash/bash'

bash:
	grep -qxF $(BASHSTR) ~/.bashrc || echo $(BASHSTR) >> ~/.bashrc

py:
	python3 ../python/usercustomize_install.py


.PHONY: link ssh fzf bash py
