import time
import math
import os
import subprocess

import redis

import sysstats_pb2
import sysstats_pb2_grpc

class SysStatsServicer(sysstats_pb2_grpc.SysStatsServicer):
    def __init__(self):
        self.redis = redis.Redis(
            host='sysstats_redis'
        )

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

    def DiskUsage(self, request, context):
        r = self.redis

        return sysstats_pb2.DiskUsageT(
            music = int(r.get('sysstats.disk.music')),
            tv = int(r.get('sysstats.disk.tv')),
            films = int(r.get('sysstats.disk.films'))
        )

    def Ifaces(self, request, context):
        try:
            # Hacks to get round the buffering on the pipe (and the fact that netstat doesn't flush it)
            # Had no luck with:
            # - reopening the pipe fd with no buffering
            # - using (g)stdbuf
            # - didn't try expect's unbuffered (not built by the stanard brew build of expect)
            sys = os.uname().sysname
            if sys == 'Darwin':
                proc = subprocess.Popen(["script", "-qF", "/dev/null", "netstat", "-ibd"], stdout=subprocess.PIPE)
            elif sys == 'Linux':
                proc = subprocess.Popen(["script", "-qf", "-c", "netstat -i", "/dev/null"], stdout=subprocess.PIPE)
            ip = proc.stdout

            return (sysstats_pb2.IfaceT(line=l) for l in iter(ip.readline, b''))
        except:
            pass
