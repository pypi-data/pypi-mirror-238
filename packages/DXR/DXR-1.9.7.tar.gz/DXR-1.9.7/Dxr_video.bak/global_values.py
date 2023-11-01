from queue import Queue

ip = "192.168.10.100"
isStart = False
server_isStart = False
push_server_isStart = False
isStart_from_url = False
url = 0
port = 5001
video_que = Queue(maxsize=1)
video_from_url_que = Queue(maxsize=1)

