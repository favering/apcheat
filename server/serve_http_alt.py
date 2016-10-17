#! /usr/bin/env python3
"""
Create http alt server on port 8080, which always redirect the request to port 80.
"""

from http.server import HTTPServer

ALT_PORT = 8080

if __name__ == '__main__':

    import sys
    sys.path.append("../")

    # instant a HTTPRequestHandler
    from public import HTTPRequestHandler
    handler = HTTPRequestHandler

    # Start HTTP ALT server
    try:
        from public import AP_IP
        httpd = HTTPServer((AP_IP, ALT_PORT), handler)
    except Exception as e:
        sys.exit('Unable to start HTTP ALT server!\n [{}]'.format(e))
    print('Started HTTP ALT server at port %d' % ALT_PORT)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

