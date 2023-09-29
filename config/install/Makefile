REL = $(shell realpath --relative-to ~ ${PWD}/..)

link:
	for i in `find ../dot -maxdepth 1 -type f,d -printf '%P\n'`; do \
		echo ln -s ../dot/$$i "~/$$i"; \
	done
	for i in `find ../dotconfig -maxdepth 1 -type f,d -printf '%P\n'`; do \
		echo ln -s "../dotconfig/$$i" "~/.config/$$i"; \
	done


vundle:
	@git clone https://github.com/VundleVim/Vundle.vim.git .vim/bundle/Vundle.vim

fzf:
	@git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
	@~/.fzf/install


.PHONY: link vundle fzf

