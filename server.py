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


# Copyright 2020 Yuxuan Zhao

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#      http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


class MyWebServer(socketserver.BaseRequestHandler):
    def setup(self):
        self.base_dir = "www"
        self.base_url = "http://{0}:{1}".format(
            self.server.server_address[0], self.server.server_address[1]
        )

    def response(self, response_status, redirect=None, file_type="html", file=None):
        self.request.sendall(
            bytearray("HTTP/1.1 {}\r\n".format(response_status), "utf-8")
        )
        if redirect:
            self.request.sendall(
                bytearray("Location: {}\r\n".format(redirect), "utf-8"))
        else:
            self.request.sendall(
                bytearray("Content-Type: text/{};\r\n".format(file_type), "utf-8")
            )
            self.request.sendall(bytearray("Connection: closed\r\n\r\n", "utf-8"))

        # if file is requested
        if file:
            self.request.sendall(bytearray(file, "utf-8"))

    def get_file_extension(self, path):
        if "." in path:
            return path.split(".")[1]
        return "html"

    def file_exists(self, path):

        if not os.path.exists(path):
            return False
        if os.path.samefile(self.base_dir, path):
            return True

        for root, dirs, files in os.walk(self.base_dir):
            for file in files:
                if os.path.samefile(os.path.join(root, file), path):
                    return True

            for directory in dirs:
                if os.path.samefile(os.path.join(root, directory), path):
                    return True
        return False

    def get_full_path(self, path):

        if path[-1] == "/":
            full_path = self.base_dir + path + "index.html"
        elif "." in path:
            full_path = self.base_dir + path
        elif path[-1] != "/":
            full_path = self.base_dir + path + "/" + "index.html"
            print("full path in get", full_path)
            if self.file_exists(full_path):
                redirect_location = (
                    self.base_url + path + "/"
                )
                self.response("301 Moved Permanently", redirect=redirect_location)
                return
            print("not exist")

        return full_path

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("Got a request of: %s\n" % self.data)

        request_method = self.data.splitlines()[0].decode().split(" ")[0]
        if request_method == "GET":
            path = self.data.splitlines()[0].decode().split(" ")[1]
            file_path = self.get_full_path(path)
            if file_path:
                if self.file_exists(file_path):
                    file = open(file_path, "r").read()
                    file_type = self.get_file_extension(path)
                    self.response("200 OK", file_type=file_type, file=file)
                else:
                    self.response("404 Not Found")

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
