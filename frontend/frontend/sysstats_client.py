import time

import grpc
import sysstats_pb2
import sysstats_pb2_grpc

channel = grpc.insecure_channel('sysstats_backend:50051')
stub = sysstats_pb2_grpc.SysStatsStub(channel)

def date():
    return time.asctime(
        time.gmtime(
            stub.Date(sysstats_pb2.Unit()).date
        )
    )

def uname_a():
    return stub.Os(sysstats_pb2.Unit()).uname_a
def kernel_version():
    return stub.Os(sysstats_pb2.Unit()).kernel_version

def ifaces():
    return stub.Ifaces(sysstats_pb2.Unit())

# TODO for the lists you wanna open the files and stream each line over grpc
# streaming, then have kinja loop the iterator
# put a delay in the sender and see what it looks like
