


import urllib.error
import urllib.request
import threading
import queue
import urllib.parse


threads = 50
target_url = "http://lms.asoiu.edu.az"
wordlist_file = "/home/samurai/Desktop/Python_For_Hacking/Web_Hackery/wordlist.txt"
resume = None
user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"


def build_wordlist(wordlist_file):

    with open(wordlist_file,"rb") as f:
        raw_words = f.readlines()
    
    found_resume = False
    words = queue.Queue()

    for word in raw_words:

        word = word.rstrip().decode('utf-8')

        if resume is not None:

            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True
                    print(f"Resuming wordlist from: {resume}")
        else:
            words.put(word)

    return words



def dir_bruter(word_queue,extensions=None):

    while not word_queue.empty():

        attempt = word_queue.get()
        attempt_list = []

        if "." not in attempt:
            attempt_list.append(f"/{attempt}/")
        else:
            attempt_list.append(f"/{attempt}")
        

        if extensions:
            for extension in extensions:
                attempt_list.append(f"/{attempt}{extension}")
        

        for brute in attempt_list:
            
            url = f"{target_url}{urllib.parse.quote(brute)}"

            try:

                headers = {}
                headers['User-Agent'] = user_agent
                
                r = urllib.request.Request(url,headers=headers)

                response = urllib.request.urlopen(r)

                if len(response.read()):
                    print(f"[{response.code}] => {url}")
            
            except urllib.error.URLError as e:

                if hasattr(e,'code') and e.code != 404:
                    print(f"!!! {e.code} => {url}")

                pass


word_queue = build_wordlist(wordlist_file)
extensions = [".php",".bak",".orig",".inc"]

for i in range(threads):
    t = threading.Thread(target=dir_bruter,args=(word_queue,extensions,))
    t.start()


