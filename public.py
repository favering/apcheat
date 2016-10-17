#! /usr/bin/env python3

# ap http server port
HTTP_PORT = 80
# ap ip address
AP_IP = "192.168.1.1"
# dhcp range
IP_ST = "192.168.1.100"
IP_ED = "192.168.1.200"

from http.server import SimpleHTTPRequestHandler

class HTTPRequestHandler(SimpleHTTPRequestHandler):
    """
    Request handler for the HTTPS/HTTP_ALT server. It responds to
    everything with a 301 redirection to the HTTP server.
    """
    def do_QUIT(self):
        """
        Sends a 200 OK response, and sets server.stop to True
        """
        self.send_response(200)
        self.end_headers()
        self.server.stop = True

    # def setup(self):
    #     self.connection = self.request
    #     self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
    #     self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)

    def do_GET(self):
        print("443/8080 do_GET")
        self.send_response(301)
        self.send_header('Location', 'http://' + AP_IP + ':' + str(HTTP_PORT))
        self.end_headers()

    def log_message(self, format, *args):
        return


