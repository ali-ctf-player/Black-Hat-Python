


from burp import IBurpExtender # type: ignore
from burp import IContextMenuFactory # type: ignore

from javax.swing import JMenuItem # type: ignore
from java.util import List,ArrayList # type: ignore
from java.net import URL # type: ignore

import socket
import urllib.parse
import json
import re
import base64




bing_api_key = "YOURKEY"

class BurpExtender(IBurpExtender,IContextMenuFactory):
    def registerExtenderCallbacks(self,callbacks):

        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()

        self.context = None

        callbacks.setExtensionName("BHP Bing")
        callbacks.registerContextMenuFactory(self)
        return
    

    def createMenuItems(self,context_menu):
        self.context_menu = context_menu
        menu_list = ArrayList()
        menu_list.add(JMenuItem("Send to Bing",actionPerformed=self.bing_menu))
        return menu_list
    

    def bing_menu(self,event):

        http_traffic = self.context.getSelectedMessages()
        print(f"{len(http_traffic)} requests highlighted")

        for traffic in http_traffic:
            http_service = traffic.getHttpService()
            host = http_service.getHost()

            print(f"User selected host: {host}")

            self.bing_search(host)
        return
    

    def bing_search(self,host):

        is_ip = re.match(r"^\d{1,3}(?:\.\d{1,3}){3}$", host)

        if is_ip:
            ip_address = host
            domain = False
        else:
            ip_address = socket.gethostbyname(host)
            domain = True
        
        bing_query_string = f"'ip:{ip_address}'"
        self.bing_query(bing_query_string)

        if domain:
            bing_query_string = f"'domain:{host}'"
            self.bing_query(bing_query_string)
    

    def bing_query(self,bing_query_string):

        print(f"Performing Bing search: {bing_query_string}")
        quoted_query = urllib.parse.quote(bing_query_string)

        http_request = f"GET /Bing/Search/Web?format=json&$top=20&Query={quoted_query} HTTP/1.1\r\n"
        headers = (
            "Host: api.datamarket.azure.com\r\n"
            "Connection: close\r\n"
            f"Authorization: Basic {base64.b64encode((':' + bing_api_key).encode()).decode()}\r\n"
            "User-Agent: Blackhat Python\r\n\r\n"
        )

        full_request = http_request + headers

        

        try:
            response = self._callbacks.makeHttpRequest("api.datamarket.azure.com",443,True,full_request)
            response_str = ''.join(map(chr,response.getResponse()))
            json_body = response_str.split("\r\n\r\n",1)[1]

            r = json.loads(json_body)

            if len(r["d"]["results"]):
                for site in r["d"]["results"]:
                    print("*" * 100)
                    print(site['Title'])
                    print(site['Url'])
                    print(site['Description'])
                    print("*" * 100)

                    j_url = URL(site['Url'])

            if not self._callbacks.isInScope(j_url):
                print("Adding to Burp scope")
                self._callbacks.includeInScope(j_url)
        except Exception as e:
            print("Error during Bing query:",str(e))
            

        return