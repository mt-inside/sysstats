docker network create service_net
docker run -d redis:latest -n service_net -n sysstats_redis
