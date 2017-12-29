import time
import math
import os
import subprocess
import shlex

import redis

import sysstats_pb2
import sysstats_pb2_grpc

def slurp(cmd):
    return "<unknown>"
    #return subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE).stdout.decode('utf-8')

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

        modules = slurp("lsmod")

        return sysstats_pb2.OsT(
            uname_a = uname,
            kernel_version = kernel,
            modules = modules
        )

    def DiskUsage(self, request, context):
        r = self.redis

        disks = ['sda', 'sdb', 'sdc', 'sdd', 'sde']
        temps = { d: slurp("/usr/sbin/hddtemp -q /dev/%s" % d) for d in disks }
        smarts = { d: slurp("/usr/sbin/smartctl -H /dev/%s" % d) for d in disks }

        return sysstats_pb2.DiskUsageT(
            free = slurp('df -h -l -T'),
            music = int(r.get('sysstats.disk.music')),
            tv = int(r.get('sysstats.disk.tv')),
            films = int(r.get('sysstats.disk.films')),
            raid = slurp('zpool status'),
            temps = temps,
            smart_statuses = smarts
        )

    def Ifaces(self, request, context):
        try:
            # Hacks to get round the buffering on the pipe (and the fact that netstat doesn't flush it)
            # Had no luck with:
            # - reopening the pipe fd with no buffering
            # - using (g)stdbuf
            # - didn't try expect's unbuffered (not built by the stanard brew build of expect)
            # - TODO: slurp this?
            sys = os.uname().sysname
            if sys == 'Darwin':
                proc = subprocess.Popen(["script", "-qF", "/dev/null", "netstat", "-ibd"], stdout=subprocess.PIPE)
            elif sys == 'Linux':
                proc = subprocess.Popen(["script", "-qf", "-c", "netstat -i", "/dev/null"], stdout=subprocess.PIPE)
            ip = proc.stdout

            return (sysstats_pb2.IfaceT(line=l) for l in iter(ip.readline, b''))
        except:
            pass

    def Users(self, request, context):
        return sysstats_pb2.UsersT(
            users=slurp("w -f")
        )

    def Mem(self, request, context):
        return sysstats_pb2.MemT(
            free=slurp("free -h")
        )

    def Containers(self, request, context):
        return sysstats_pb2.ContainersT(
            containers=slurp("docker ps")
        )

#
#title "Temperatures"
#
#out sensors
#
#
#title "Network"
#
##Requires root
##out /sbin/iptables -L -v -n
#
#out netstat -i
#
#out netstat -r -n
#
#title "Hardware"
#
#out lsscsi
#
#out lsusb
#
#out lscpu
#
#out /usr/sbin/lspci
