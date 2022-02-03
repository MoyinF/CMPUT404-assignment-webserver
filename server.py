#  coding: utf-8
import socketserver
from datetime import datetime
import os
from pathlib import Path
import mimetypes
from email.message import EmailMessage

mimetypes.add_type("text/css", ".css", True)
mimetypes.add_type("text/html", ".html", True)


# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/



class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        self.date = datetime.now()
        self.date = self.date.strftime("%a, %d %b %y %H:%M:%S GMT")
        self.decoded = self.data.decode()
        self.decoded_list = self.decoded.split()
        self.data_folder = "www"
        self.fname = self.decoded_list[1]
        self.path = self.data_folder + self.fname
        self.isfile = os.path.exists(self.path)
        self.filetype = mimetypes.guess_type(self.path)[0]
        self.content_length = len(self.decoded)
        self.url_change = False


        if self.filetype is None and self.path[-1] != "/":
            self.path = self.path + "/"
            self.url_change = True
            self.new_url = "http://127.0.0.1:8080" + self.fname + "/"
        if "hardcode" in self.fname:
            self.filetype = "text/html"


        if self.decoded_list[0] == "GET":
            if self.path[:18] == "www/../../../../..":
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found \r\n",'utf-8'))
                self.request.sendall(bytearray("Date: {}\r\n".format(self.date),'utf-8'))
                self.request.sendall(bytearray("Server: http://127.0.0.1:8080/\r\n",'utf-8'))
                self.request.sendall(bytearray("Content-Length: {}\r\n".format(self.content_length),'utf-8'))
                self.request.sendall(bytearray("Connection: close\r\n",'utf-8'))

            elif self.url_change and self.isfile:
                self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently \r\n",'utf-8'))
                self.request.sendall(bytearray("Date: {}\r\n".format(self.date),'utf-8'))
                self.request.sendall(bytearray("Server: http://127.0.0.1:8080/\r\n",'utf-8'))
                self.request.sendall(bytearray("Location: {}\r\n".format(self.new_url),'utf-8'))
                self.request.sendall(bytearray("Connection: close\r\n",'utf-8'))


            elif self.isfile:
                self.request.sendall(bytearray("HTTP/1.1 200 OK \r\n",'utf-8'))
                self.request.sendall(bytearray("Date: {}\r\n".format(self.date),'utf-8'))
                self.request.sendall(bytearray("Server: http://127.0.0.1:8080/\r\n",'utf-8'))
                self.request.sendall(bytearray("Content-Length: {}\r\n".format(self.content_length),'utf-8'))
                self.request.sendall(bytearray("Content-Type: {}\r\n".format(self.filetype),'utf-8'))
                self.request.sendall(bytearray("Connection: close\r\n",'utf-8'))

            else:
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found \r\n",'utf-8'))
                self.request.sendall(bytearray("Date: {}\r\n".format(self.date),'utf-8'))
                self.request.sendall(bytearray("Server: http://127.0.0.1:8080/\r\n",'utf-8'))
                self.request.sendall(bytearray("Content-Length: {}\r\n".format(self.content_length),'utf-8'))
                self.request.sendall(bytearray("Connection: close\r\n",'utf-8'))




        else:
            self.request.sendall(bytearray("HTTP/1.1 405 Not Found \r\n",'utf-8'))
            self.request.sendall(bytearray("Date: {}\r\n".format(self.date),'utf-8'))
            self.request.sendall(bytearray("Server: http://127.0.0.1:8080/\r\n",'utf-8'))
            self.request.sendall(bytearray("Content-Length: {}\r\n".format(self.content_length),'utf-8'))
            self.request.sendall(bytearray("Connection: close\r\n",'utf-8'))
            


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    # port = 80

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)


    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
