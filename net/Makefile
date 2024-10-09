
run:
	PYTHONPATH=. python3 -m bwninja.tui

install-editable:
	python3 -m pip install -e .

install-deps:
	sudo apt install python3-bpfcc

install-publish-deps:
	python3 -m pip install build twine 'setuptools>=68'

publish: clean
	python3 -m build --no-isolation
	python3 -m twine upload dist/*

clean:
	-rm dist/ -rf
	-rm build/ -rf
	-rm *.egg-info/ -rf
	-rm __pycache__ -rf
