

import re
import zlib
import os
import cv2
from scapy.all import TCP,rdpcap


pictures_directory = "/home/samurai/Desktop/Python_For_Hacking/Scapy/pictures_directory"
faces_directory = "/home/samurai/Desktop/Python_For_Hacking/Scapy/faces"
pcap_file = "/home/samurai/Desktop/Python_For_Hacking/Scapy/bhp.pcap"


os.makedirs(pictures_directory,exist_ok=True)
os.makedirs(faces_directory,exist_ok=True)



def get_http_headers(http_payload):

    try:
        
        headers_raw =  http_payload[:http_payload.index("\r\n\r\n") + 4]
        headers = dict(re.findall(r"(.*?): (.*?)\r\n",headers_raw))

    except:
        return None
    
    if "Content-Type" not in headers:
        return None
    
    return headers


def extract_image(headers,http_payload):

    image = None
    image_type = None


    try:

        if "image" in headers['Content-Type']:

            image_type = headers['Content-Type'].split("/")[1]

            image = http_payload[http_payload.index("\r\n\r\n") +4:]
            image = image.encode('utf-8','ignore')


            try:

                if "Content-Encoding" in headers.keys():
                    if headers['Content-Encoding'] == "gzip":
                        image = zlib.decompress(image,16+zlib.MAX_WBITS)
                    elif headers['Content-Encoding'] == "deflate":
                        image = zlib.decompress(image)
            
            except:
                pass

    except:
        return None,None
    
    return image,image_type



def face_detect(path,file_name):

    img = cv2.imread(path)

    if img is None:
        return False
    

    cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

    rects = cascade.detectMultiScale(img,scaleFactor=1.3,minNeighbors=4,minSize=(20,20))

    if len(rects) == 0:
        return False
    

    for x1,y1,x2,y2 in rects:
        cv2.rectangle(img,(x1,y1),(x1 + x2,y1 + y2),(127,255,0),2)
    
    cv2.imwrite(f"{faces_directory}/{pcap_file}-{file_name}",img)

    return True




def http_assembler(pcap_file):

    carved_images = 0
    faces_detected = 0

    a = rdpcap(pcap_file)

    sessions = a.sessions()

    for session in sessions:
        
        http_payload = ""

        for packet in sessions[session]:

            try:
                if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                    
                    http_payload += str(packet[TCP].payload)
            
            except:
                pass

        headers = get_http_headers(http_payload)

        if headers is None:
            continue
        
        image,image_type = extract_image(headers,http_payload)


        if image is not None and image_type is not None:

            file_name = f"{pcap_file}-pic_carver_{carved_images}.{image_type}"
            file_path = os.path.join(pictures_directory,file_name)

            with open(file_path,"wb") as f:
                f.write(image)
            

            carved_images += 1

            try:

                result = face_detect(f"{pictures_directory}/{file_name}",file_name)

                if result is True:
                    faces_detected += 1
            except:
                pass


    return carved_images, faces_detected


carved_images, faces_detected = http_assembler(pcap_file)

print(f"Extracted: {carved_images} images")
print(f"Detected: {faces_detected} faces")



