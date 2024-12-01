
all:
	@echo "\n\nRun instead:\n  make perfetto && make protos"

perfetto: build/perfetto/BUILD

build/perfetto/BUILD: build
	cd build &&\
		git clone --depth 1 https://github.com/google/perfetto.git
	# set mtime instead using git mtime
	touch $@


PROTOS := $(shell cd build/perfetto; find protos -type f -name "*.proto" -exec echo {} \;)
PB2S := $(foreach proto, $(PROTOS), $(patsubst %.proto, rebugger/%_pb2.py, $(proto)))

protos: $(PB2S)

rebugger/protos/%_pb2.py: build/bin/protoc
	build/bin/protoc \
		--python_out=rebugger \
		--proto_path=build/perfetto \
		$(patsubst rebugger/%_pb2.py, %.proto, $@)

build:
	mkdir -p build


build/bin/protoc: build
	# version must not be newer than python-pip installed proto runtime version
	cd build &&\
		wget https://github.com/protocolbuffers/protobuf/releases/download/v28.3/protoc-28.3-linux-x86_64.zip &&\
		unzip *.zip
	# set mtime instead using git mtime
	touch $@


clean_protos:
	-rm build -rf
	-rm rebugger/protos -rf


install-editable:
	python3 -m pip install -e .


clean:
	-rm dist/ -r
	-rm *.egg-info/ -r


publish: clean
	python3 -m build --sdist --no-isolation
	python3 -m twine upload dist/*
