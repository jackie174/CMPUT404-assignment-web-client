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

from base64 import encode
import sys
import socket
# you may use urllib to encode data appropriately
from urllib.parse import urlparse
import urllib.parse


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

    def get_code(self, data):
        header, body = data.split("\r\n\r\n")
        code = header.split(" ")[1]
        return int(code)

    def get_headers(self,data):
        header, body = data.split("\r\n\r\n")
        return header

    def get_body(self, data):
        header, body = data.split("\r\n\r\n")
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

    def GET(self, url, args=None):
        try:
            url_parse = urlparse(url)
            hostname=url_parse.hostname
            port = url_parse.port
            path = url_parse.path
            query=url_parse.query
            #check invalid path, port
            path = path if len(path)!=0 else "/"
            port = port if port is not None else 80
            self.connect(hostname, port)
            if args is None:
                request = "GET {} HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n".format(path, hostname)
                self.sendall(request)
                data = self.recvall(self.socket) 
                code = self.get_code(data)
                body = self.get_body(data)
                self.close()
                return HTTPResponse(code, body)
            else:
                path = path+'?'+query
                request = "GET {} HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n".format(path, hostname)
                self.sendall(request)
                data = self.recvall(self.socket)
                code = self.get_code(data)
                body = self.get_body(data)
                self.close()
                return HTTPResponse(code, body)


        except:
            print("Url is incorectly!")
            return 

    def POST(self, url, args=None):
        try:
            url_parse = urlparse(url)
            hostname=url_parse.hostname
            port = url_parse.port
            path = url_parse.path
            path = path if len(path)!=0 else "/"
            port = port if port is not None else 80
            self.connect(hostname, port)
            if args is None:
                request = "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Type: {}\r\nContent-Length: {}\r\nConnection: close\r\n\r\n".format(path, hostname, 'application/x-www-form-urlencoded', 0)
                self.sendall(request)
                data = self.recvall(self.socket)
                code = self.get_code(data)
                body = self.get_body(data)
                self.close()
                return HTTPResponse(code, body)
            else:
                encoded_args= urllib.parse.urlencode(args)
                request = "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Type: {}\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{}".format(path, hostname, 'application/x-www-form-urlencoded', len(encoded_args), encoded_args)
                self.sendall(request)
                data = self.recvall(self.socket)
                code = self.get_code(data)
                body = self.get_body(data)
                self.close()
                return HTTPResponse(code, body)


        except:
            print("Url is incorectly!")
            return 

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
