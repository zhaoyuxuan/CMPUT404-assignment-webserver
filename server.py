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
    
    def response(self, response_status, file=None):
        self.request.sendall(bytearray("HTTP/1.1 {}".format(response_status),'utf-8'))
        self.request.sendall(bytearray("Content-Type: text/html;",'utf-8'))
        self.request.sendall(bytearray("Connection: closed",'utf-8'))

        # if file is requested
        if file:
            self.request.sendall(bytearray(file,'utf-8'))

    def get_file(self, path):
        # remove the leading slash
        path = path[1:]

        # if the path is not slash
        if path
            # check if file on server
            try:
                file = open('www'+path)
            except:
                return None
            else:
                return file
        else:
            file = open('www'+'index.html')
            return path,file
            
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        
        request_method = self.data.splitlines()[0].decode().split(" ")[0]

        if request_method == "GET":
            path = self.data.splitlines()[0].decode().split(" ")[1]
            file_path,file = self.get_file(path)

            file = open(file_path).read()

            self.request.sendall(bytearray("HTTP/1.1 200 OK",'utf-8'))
            self.request.sendall(bytearray("Content-Type: text/html",'utf-8'))
            self.request.sendall(bytearray("Connection: closed",'utf-8'))                
            self.request.sendall(bytearray(file.read(),'utf-8'))

        # Request method is not GET, return 405
        else:
            self.response("405 Method Not Allowed")
            
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
