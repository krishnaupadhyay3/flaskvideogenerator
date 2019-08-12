
import redis
from rq import Worker, Queue, Connection
import os
import uuid
def RunFFmpeg(data):
    src_path = data["src_path"]
    time_duration = data["time_duration"]
    dst_path = os.path.splitext(src_path)[0]+str(uuid.uuid4())+".mp4"
    command = ["/usr/bin/ffmpeg","-i","%s"%src_path,"%s"%dst_path]

    cmd = " ".join(command)
    print(cmd)
    handle = os.popen(cmd) 
    line = " "
    while line:
        line = handle.read()
        print (line)
    handle.close()
listen = ['default']

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
