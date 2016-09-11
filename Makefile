REL = $(shell realpath --relative-to ~ ${PWD})

install:
	@ln -s $(REL)/.gitconfig ~/.gitconfig



.PHONY: install

