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