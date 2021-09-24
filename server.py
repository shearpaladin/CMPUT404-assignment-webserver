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

        #https: // stackoverflow.com/questions/606191/convert-bytes-to-a-string
        print(self.data.decode("utf-8"))
        # .split(' ') turns an object into an array of elements splitting items where there is a space
        http_headers = self.data.decode("utf-8").split("\r\n")[0].split(" ")
        http_method = http_headers[0] # grab first item in our array
        path = http_headers[1]
        print(http_headers)
        print("HTTP_METHOD:" + http_method)
        print("PATH:"+ path)
        
        # Returned the path of where this program was located.
        # https://stackoverflow.com/questions/3430372/how-do-i-get-the-full-path-of-the-current-files-directory
        project_directory = os.path.dirname(os.path.abspath(__file__))
        print(project_directory)


        # If GET Request then go to index.html
        if (http_method == "GET"):
        # Prevent access to parent directory / check if it exists
            if ".." in path.split("/"):
                self.status_404()


        
        else:
            self.status_405()


    
    # 200: Ok
    def status_200(self):
        status = "HTTP/1.1 200 OK" + "\r\n"
        self.request.sendall(bytearray(status, 'utf-8'))


    ############################ ERROR CODES ##################################################
    # 301: Moved Permanently
    def status_301(self):
        status = "HTTP/1.1 301 Moved Permanently" + "\r\n"
        self.request.sendall(bytearray(status, 'utf-8'))

    # 404: Not Found
    def status_404(self):
        status = "HTTP/1.1 404 Not Found" + "\r\n"
        self.request.sendall(bytearray(status, 'utf-8'))

    # 405: Method Not Allowed
    def status_405(self):
        status = "HTTP/1.1 405 Method Not Allowed" + "\r\n"
        self.request.sendall(bytearray(status,'utf-8'))

        

    



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
