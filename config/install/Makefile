REL = $(shell realpath --relative-to ~ ${PWD}/..)

link:
	@for i in `ls "$(REL)/dot/*"`; do \
		echo ln -s $(REL)/dot/$i ~/$i; \
	done

	@for i in `ls "$(REL)/dotconfig/*"`; do \
		echo ln -s $(REL)/dotconfig/$i ~/.config/$i; \
	done


vundle:
	@git clone https://github.com/VundleVim/Vundle.vim.git .vim/bundle/Vundle.vim

fzf:
	@git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
	@~/.fzf/install


.PHONY: link vundle fzf

