import time
from concurrent import futures

import grpc
import sysstats_pb2_grpc
from sysstats_server import SysStatsServicer

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sysstats_pb2_grpc.add_SysStatsServicer_to_server(SysStatsServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    print("Starting...")
    serve()
