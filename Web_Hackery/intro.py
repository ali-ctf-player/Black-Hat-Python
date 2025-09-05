


import urllib.request

#body = urllib.request.urlopen("http://lms.asoiu.edu.az")

#print(body.read())



url = "http://lms.asoiu.edu.az"

headers = {}
headers['User-Agent'] = "Googlebot"

request = urllib.request.Request(url,headers=headers)

response = urllib.request.urlopen(request)

print(response.read().decode('utf-8'))

response.close()
