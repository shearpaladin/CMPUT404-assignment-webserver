#  coding: utf-8 
import socketserver
import os

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

        #print(self.data.decode("utf-8"))

        #https: // stackoverflow.com/questions/606191/convert-bytes-to-a-string
        self.method = self.data.decode("utf-8").split(' ')[0]  # grab METHOD
        self.file_name = self.data.decode("utf-8").split(" ")[1]  # grab file/name
        self.url = os.path.abspath(__file__)
        self.home_dir = os.path.dirname(self.url)
        

        if (self.method == "GET"):


            if (os.path.exists(self.home_dir + '/www' + self.file_name) and (".." not in self.file_name.split("/"))):
                
                if (self.file_name) == "/deep":
                    self.send_response(301)
                    return

                # http://127.0.0.1:8080/ 
                if (self.file_name.endswith("/")):
                    self.url = self.home_dir + '/www' + self.file_name + "index.html"
                
                else:
                    self.url= self.home_dir + '/www' + self.file_name
            
            else:
                self.send_response(404)


            # if file requested: base.css index.html
            if os.path.isdir("/www" + self.file_name): # /www/deep
                self.url= self.file_name + "index.html"
            self.content_type = self.url.split(".")[-1] #grab css or html 
            self.send_response(200)
  
        # for post/put/delete
        else:
            self.send_response(405)
        
    def send_response(self, status_code):

        # 405: Method Not Allowed
        if status_code == 405:
            self.request.sendall(
                bytearray("HTTP/1.1 405 Method Not Allowed\r\n\r\n" + "<html><h1><405 Method Not Allowed</h1><body></body></html>", "utf-8"))

        # 404: Not Found
        elif status_code == 404:
            self.request.sendall(
                bytearray("HTTP/1.1 404 Not Found\r\n\r\n" + "<html><h1>404 Not Found</h1><body></body></html>", "utf-8"))

        # 301 Moved Permanently
        elif status_code == 301:
            self.request.sendall(
            bytearray("HTTP/1.1 301 Moved Permanently\r\n\r\n", "utf-8"))
            self.request.sendall(
                bytearray("Location: http://127.0.0.1:8080/deep/\n" + "<html><h1>301 Moved Permanently</h1></html>" + "\n", "utf-8"))

        # 200: Ok
        elif status_code == 200:
            self.content = open(self.url, 'r').read()
            self.request.sendall(
                bytearray("HTTP/1.1 200 OK"+"\r\n" +"Content-Type: text/"+ self.content_type + "\r\n\r\n", 'utf-8'))
            self.request.sendall(bytearray(self.content + "\n\n", 'utf-8'))
    


       

        

        

    



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
