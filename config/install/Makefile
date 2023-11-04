REL = $(shell realpath --relative-to ~ ${PWD}/..)
HOME = $(shell echo ~)

all: ssh link bash fzf

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


ssh:
	cp -R ~/.ssh ~/.ssh.bak
	mv ~/.ssh/* ../dot/.ssh/
	rm -r ~/.ssh

fzf:
	@git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
	@~/.fzf/install


BASHSTR = '[ -f ~/knio/config/bash/bash ] && source ~/knio/config/bash/bash'

bash:
	grep -qxF $(BASHSTR) ~/.bashrc || echo $(BASHSTR) >> ~/.bashrc


.PHONY: link ssh fzf bash
