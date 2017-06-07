python -m grpc_tools.protoc -I../protos --python_out=frontend --grpc_python_out=frontend ../protos/sysstats.proto

docker build . -t sysstats_frontend
