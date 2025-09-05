

from burp import IBurpExtender  # type:ignore
from burp import IContextMenuFactory  # type: ignore

from javax.swing import JMenuItem  # type: ignore
from java.util import List, ArrayList  # type: ignore
from java.net import URL  # type: ignore

import re
from datetime import datetime




class TagStripper(object):
    def strip(self, html):
        # Remove script and style tags and their content
        html = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<style.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
        # Remove HTML tags
        html = re.sub(r'<[^>]+>', ' ', html)
        # Remove multiple spaces
        html = re.sub(r'\s+', ' ', html)
        return html.strip()
    

class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self.context = None
        self.hosts = set()

        self.wordlist = set(["password"])

        callbacks.setExtensionName("BHP Wordlist")
        callbacks.registerContextMenuFactory(self)

        return
    
    def createMenuItems(self, context_menu):
        self.context = context_menu
        menu_list = ArrayList()
        menu_list.add(JMenuItem("Create Wordlist", actionPerformed=self.wordlist_menu))
        return menu_list

    def wordlist_menu(self, event):
        http_traffic = self.context.getSelectedMessages()

        for traffic in http_traffic:
            http_service = traffic.getHttpService()
            host = http_service.getHost()

            self.hosts.add(host)

            http_response = traffic.getResponse()

            if http_response:
                self.get_words(http_response)
            
        self.display_wordlist()
        return
    
    def get_words(self, http_response):
        headers, body = self._helpers.bytesToString(http_response).split("\r\n\r\n", 1)

        if "content-type: text" not in headers.lower():
            return
        
        tag_stripper = TagStripper()
        page_text = tag_stripper.strip(body)

        words = re.findall(r"[a-zA-Z]\w{2,}", page_text)

        for word in words:
            if len(word) <= 12:
                self.wordlist.add(word.lower())
        
        return
    
    def mangle(self, word):
        year = datetime.now().year
        suffixes = ["", "1", "!", str(year)]
        mangled = []

        for password in (word, word.capitalize()):
            for suffix in suffixes:
                mangled.append("%s%s" % (password, suffix))  # Replaced f-string with % formatting
        
        return mangled
    
    def display_wordlist(self):
        print("#!comment: BHP Wordlist for site(s) %s" % ", ".join(self.hosts))  # Replaced f-string with % formatting

        for word in sorted(self.wordlist):
            for password in self.mangle(word):
                print(password)
        
        return