#! /usr/bin/env python3
"""
Create https server on port 443, which always redirect the request to port 80.
"""

from http.server import HTTPServer
from socketserver import TCPServer
import ssl

SSL_PORT = 443
PEM = "https_server.pem"

class SecureHTTPServer(HTTPServer):
    """
    Simple HTTPS server that extends the HTTPServer standard
    module to support the SSL protocol.
    """
    def __init__(self, server_address, HandlerClass):
        TCPServer.__init__(self, server_address, HandlerClass)
        self.socket = ssl.wrap_socket(self.socket, server_side=True, certfile=PEM, ssl_version=ssl.PROTOCOL_TLSv1_2)
        # self.server_bind()
        # self.server_activate()

    def serve_forever(self):
        """
        Handles one request at a time until stopped.
        """
        self.stop = False
        while not self.stop:
            self.handle_request()

if __name__ == '__main__':

    import sys
    sys.path.append("../")

    # instant a HTTPRequestHandler
    from public import HTTPRequestHandler
    handler = HTTPRequestHandler

    # Start HTTPS server
    try:
        from public import AP_IP
        httpd = SecureHTTPServer((AP_IP, SSL_PORT), handler)
    except Exception as e:
        sys.exit('Unable to start HTTPS server!\n [{}]'.format(e))
    print('Started HTTPS server at port %d' % SSL_PORT)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

