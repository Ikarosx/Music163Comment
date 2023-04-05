import redis
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password='newLife2016')
r = redis.Redis(connection_pool=pool)
while True:
    url = r.rpop("Music163:request")
    if url:
        r.rpush("Music163:requests", url)
        continue
    break
