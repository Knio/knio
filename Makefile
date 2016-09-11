REL = $(shell realpath --relative-to ~ ${PWD})

install:
	@-ln -s $(REL)/.gitconfig ~/.gitconfig
	@-ln -s $(REL)/.vim ~/.vim
	@-ln -s $(REL)/.aliases ~/.aliases

.PHONY: install

