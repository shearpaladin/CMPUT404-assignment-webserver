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
        http_headers = self.data.decode("utf-8").split("\r\n")[0].split(" ")
        http_method = http_headers[0] # grab METHOD
        file_path = http_headers[1] # grab FILE_PATH

        
        if (self.check_method(http_method) == False):
            self.status_405()
        
        if (self.check_path(file_path) == False):
            self.status_404()
        
        self.send_response()
        
            
    def check_method(self, http_method):
        if (http_method == "GET"):
            return True
        return False
    
    def check_path(self, file_path):
        if (self.check_depth() == False or "../" in file_path):
            return False
        return True
       


    #https: // security.openstack.org/guidelines/dg_using-file-paths.html
    #https: // www.tutorialspoint.com/python3/os_getcwd.htm
    #https: // www.w3schools.com/python/ref_string_startswith.asp
    # Serve ONLY files in ./www and deeper

    def check_depth(self):
        base_dir = os.getcwd() + "/www"
        return os.path.realpath("./www").startswith(base_dir)
        

    def send_response(self):

        # 405: Method Not Allowed
        if self.status_code == 405:
            status_line = "HTTP/1.1 405 Method Not Allowed" + "\r\n"
            self.request.sendall(bytearray(status_line, 'utf-8'))

        # 404: Not Found
        elif self.status_code == 404:
            status_line = "HTTP/1.1 404 Not Found" + "\r\n"
            self.request.sendall(bytearray(status_line, 'utf-8'))

        # 301 Moved Permanently
        elif self.status_code == 301:
            status_line = "HTTP/1.1 301 Moved Permanently" + "\r\n"
            self.request.sendall(bytearray(status_line, 'utf-8'))
            
        # 200: Ok
        elif self.status_code == 200:
            status_line = "HTTP/1.1 200 OK" + "\r\n"
            self.request.sendall(bytearray(status_line, 'utf-8'))
    


       

        

        

    



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
