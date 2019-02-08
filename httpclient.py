#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
#https://docs.python.org/3/library/urllib.parse.html
import urllib.parse
from urllib.parse import urlparse


#external source code references:
#https://blog.csdn.net/liu915013849/article/details/78869771
#by wiiknow

#https://docs.python.org/3/library/socket.html

#https://blog.csdn.net/ydyang1126/article/details/75050175
#by Moxiao

#https://docs.python.org/3/library/urllib.parse.html

#https://github.com/sjpartri/CMPUT404-assignment-web-client/blob/master/httpclient.py
#by Sean Partridge sjpartri

#https://github.com/sam9116/CMPUT404-assignment-web-client/blob/master/httpclient.py
#by Sam Bao sam9116

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None
    #https://blog.csdn.net/ydyang1126/article/details/75050175 by Moxiao
    def get_code(self, data):
        data_elements = data.split('\r\n\r\n')
        header = data_elements[0].split('\r\n')
        code_final = int(header[0].split(' ')[1])
        return code_final

    def get_headers(self,data):
        return None

    def get_body(self, data):
        data_elements = data.split('\r\n\r\n')
        body = data_elements[1]
        return body

    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))

    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    #https://github.com/sjpartri/CMPUT404-assignment-web-client/blob/master/httpclient.py
    #by Sean Partridge sjpartri

    #https://github.com/sam9116/CMPUT404-assignment-web-client/blob/master/httpclient.py
    #by Sam Bao sam9116
    def send_request(self,request,host,path,encode_url):

        if request == "GET":
            request_text = "GET "+path+" HTTP/1.1\r\n"\
                            "Host: "+host+"\r\n"\
                            "Accept: */*\r\n\r\n"
        elif request == "POST":
            request_text = "POST "+path+" HTTP/1.1 \r\n"\
                            "Host: "+host+"\r\n"\
                            "Accept: */* \r\n"\
                            "Content-Length: "+str(len(encode_url))+" \r\n"\
                            "Content-Type: application/x-www-form-urlencoded\r\n\r\n"+encode_url +" \r\n"

        return request_text

    def get_parse(self,url):
        #https://docs.python.org/3/library/urllib.parse.html
        o = urlparse(url)
        #https://blog.csdn.net/ydyang1126/article/details/75050175
        #Moxiao
        netloc = o.netloc
        urls = netloc.split(':',1)
        host = urls[0]

        port = o.port
        if (port == None):
            port = 80

        path = o.path
        if(path==''):
            path='/'

        return host,port,path

    def GET(self, url, args=None):
        code = 500
        body = ""
        host,port,path = self.get_parse(url)
        self.connect(host,port)
        request_text = self.send_request("GET",host,path,"N/A")
        self.sendall(request_text)
        data_recvall = self.recvall(self.socket)

        code = self.get_code(data_recvall);
        body = self.get_body(data_recvall);

        self.close()

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        host,port,path = self.get_parse(url)
        self.connect(host,port)

        if(args == None):
            args = ''
        encode_url = urllib.parse.urlencode(args)

        request_text = self.send_request("POST",host,path,encode_url)
        self.sendall(request_text)
        data_recvall = self.recvall(self.socket)

        data_recvall_length = len(data_recvall.split('\r\n\r\n'))
        if(data_recvall_length>1):
            body = self.get_body(data_recvall);
        code = self.get_code(data_recvall);

        self.close()

        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )

if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
