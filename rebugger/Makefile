

PROTOS := $(shell cd build/perfetto; find protos -type f -name "*.proto" -exec echo {} \;)
PB2S := $(foreach proto, $(PROTOS), $(patsubst %.proto, %_pb2.py, $(proto)))

protos: $(PB2S)

protos/%_pb2.py: build/bin/protoc build/perfetto/BUILD
	build/bin/protoc \
		--python_out=. \
		--proto_path=build/perfetto \
		$(patsubst %_pb2.py, %.proto, $@)


build/t:
	mkdir -p build
	touch $@


build/bin/protoc: build/t
	# version must not be newer than python-pip installed proto runtime version
	cd build; wget https://github.com/protocolbuffers/protobuf/releases/download/v28.3/protoc-28.3-linux-x86_64.zip
	cd build; unzip *.zip
	touch $@


build/perfetto/BUILD: build/t
	cd build; git clone --depth 1 https://github.com/google/perfetto.git


clean_protos:
	-rm build -rf
	-rm protos -rf


install-editable:
	python3 -m pip install -e .


clean:
	-rm dist/ -r
	-rm *.egg-info/ -r


publish: clean
	python3 -m build --sdist --no-isolation
	python3 -m twine upload dist/*
