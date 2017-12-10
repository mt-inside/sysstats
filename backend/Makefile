build-venv:
	python3 -m venv venv-build
	source venv-build/bin/activate
	pip3 install -r requirements.build.txt
	deactivate

grpc-stubs: build-venv
	python -m grpc_tools.protoc --proto_path protos --python_out=backend --grpc_python_out=backend protos/sysstats.proto

container:
	docker build . -t sysstats_backend

run-dev:
	docker run --rm --name sysstats_backend -v ${PWD}:/usr/src/app sysstats_backend

local-run-venv:
	python3 -m venv venv-run
	source venv-run/bin/activate
	pip3 install -r requirements.txt
	deactivate

local-run: local-run-venv
	python backend

.PHONY: build-venv grpc-stubs container run-dev local-run-venv local-run
