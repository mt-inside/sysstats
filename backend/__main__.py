import time
import math
import os
from concurrent import futures
import subprocess

import grpc

import sysstats_pb2
import sysstats_pb2_grpc

class SysStatsServicer(sysstats_pb2_grpc.SysStatsServicer):
    def Date(
        self,
        request, # dict of the args
        context # call info like timeout
    ):
        return sysstats_pb2.DateT(
            date = math.trunc(time.time())
        )

    def Os(self, request, context):
        u = os.uname()
        uname = sysstats_pb2.UnameT(nodename=u.nodename, sysname=u.sysname, release=u.release, version=u.version, machine=u.machine)

        kernel = "<unknown /proc/version>"
        try:
            ver = open('/proc/version')
        except IOError:
            pass # not on Mac for example
        else:
            with ver:
                kernel = ver.read()


        return sysstats_pb2.OsT(
            uname_a = uname,
            kernel_version = kernel
        )

    def Ifaces(self, request, context):
        try:
            TODO do a popen and don't wait for the process to complete, see if the page progressively renders
            cp = subprocess.run(["netstat", "-ibd"], stdout=subprocess.PIPE)
            ls = cp.stdout.decode().split('\n')
            return (sysstats_pb2.IfaceT(line=l) for l in ls)
        except:
            pass

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
    serve()
