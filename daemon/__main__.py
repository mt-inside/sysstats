import time

import redis

print("Starting...")

r = redis.Redis(
    host='sysstats_redis'
)

while True:
    r.set('sysstats.disk.music', 1234)
    r.set('sysstats.disk.tv', 12345)
    r.set('sysstats.disk.films', 123456)

    # this wants to be a k8s cronjob
    time.sleep(86400)
