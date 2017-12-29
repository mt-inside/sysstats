FROM python:3 as builder
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.build.txt
RUN python -m grpc_tools.protoc --proto_path protos --python_out=backend --grpc_python_out=backend protos/sysstats.proto

FROM python:3
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
COPY --from=builder /usr/src/app/backend/sysstats_pb2.py backend/sysstats_pb2.py
COPY --from=builder /usr/src/app/backend/sysstats_pb2_grpc.py backend/sysstats_pb2_grpc.py
EXPOSE 50051
CMD [ "python3", "backend" ]
