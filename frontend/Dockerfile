FROM python:3 as builder
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.build.txt
RUN python -m grpc_tools.protoc -Iprotos/vendored --python_out=frontend --grpc_python_out=frontend protos/vendored/sysstats.proto

FROM python:3
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
COPY --from=builder /usr/src/app/frontend/sysstats_pb2.py frontend/sysstats_pb2.py
COPY --from=builder /usr/src/app/frontend/sysstats_pb2_grpc.py frontend/sysstats_pb2_grpc.py
EXPOSE 3031
WORKDIR /usr/src/app/frontend
CMD [ "uwsgi", "--ini", "../uwsgi_gateway.ini" ]
#CMD [ "uwsgi", "--ini", "uwsgi_http.ini" ]
