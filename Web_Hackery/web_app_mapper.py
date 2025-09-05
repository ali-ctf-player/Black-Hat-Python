


import queue
import threading
import os
import urllib.error
import urllib.request


threads = 10

target = "http://lms.asoiu.edu.az"
directory = "/home/samurai/Desktop/Python_For_Hacking/Web_Hackery/web_files"
filters = ['.jpg','.gif','png','.css']

os.chdir(directory)

web_paths = queue.Queue()

for r,d,f in os.walk("."):

    for files in f:
        
        remote_path = f"{r}/{files}"
        if remote_path.startswith("."):
            remote_path = remote_path[1:]
        if os.path.splitext(files)[1] not in filters:
            web_paths.put(remote_path)


def test_remote():

    while not web_paths.empty():

        path = web_paths.get()
        url = f"{target}{path}"

        request = urllib.request.Request(url)

        try:
            response = urllib.request.urlopen(request)

            print(f"[{response.code}] => {path}")
            response.close()

        except urllib.error.HTTPError as error:
            print(f"[{error.code}] Not found: {url}")
        except urllib.error.URLError as e:
            print(f"[ERROR] Could not connect to {url}:{e.reason}")



for i in range(threads):
    
    print(f"Spawning thread: {i}")
    t = threading.Thread(target=test_remote)
    t.start()