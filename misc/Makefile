REL = $(shell realpath --relative-to ~ ${PWD})

link:
	@ln -s $(REL)/.gitconfig ~/.gitconfig
	@ln -s $(REL)/.vim ~/.vim

unlink:
	if [ "$(shell readlink ~/.gitconfig)" = "config/.gitconfig" ]; then rm ~/.gitconfig; fi;
	if [ "$(shell readlink ~/.vim)"       = "config/.vim"       ]; then rm ~/.vim;       fi;

vundle:
	@git clone https://github.com/VundleVim/Vundle.vim.git .vim/bundle/Vundle.vim

fzf:
	@git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
	@~/.fzf/install


.PHONY: link unlink vundle fzf

