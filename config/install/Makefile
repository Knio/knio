REL = $(shell realpath --relative-to ~ ${PWD}/..)
HOME = $(shell echo ~)

link:
	@for i in `find ~/$(REL)/dot -maxdepth 1 -type f,d -printf '%P\n'`; do \
		ln -s "$(REL)/dot/$$i" "$(HOME)/$$i"; \
	done
	@for i in `find ~/$(REL)/dotconfig -maxdepth 1 -type f,d -printf '%P\n'`; do \
		ln -s "$(REL)/dotconfig/$$i" "$(HOME)/.config/$$i"; \
	done


vundle:
	@git clone https://github.com/VundleVim/Vundle.vim.git .vim/bundle/Vundle.vim

fzf:
	@git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
	@~/.fzf/install


.PHONY: link vundle fzf

