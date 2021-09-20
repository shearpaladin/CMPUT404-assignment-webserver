#  coding: utf-8 
import socketserver

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

        # Find what type of Request we are getting
        # VALID: GET
        # INVALID: POST/PUT/DELETE return a 405
        print(self.data.decode("utf-8"))
        # .split(' ') turns an object into an array of elements splitting items where there is a space
        request_type = self.data.decode("utf-8").split(' ')[0] # grab first item in our array
        print(request_type) # Returns GET
       


        #self.request.sendall(bytearray("OK",'utf-8'))
    
    # 200: Request Succeeded
    def status_200(self):
        pass

    # 301: Moved Permently
    def status_301(self):
        pass

    # 404: Not Found
    def status_404(self):
        pass

    # 405: Method Not Allowed
    def status_405(self):
        pass

    



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
