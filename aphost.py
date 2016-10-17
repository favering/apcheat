#! /usr/bin/env python3
"""
Script to create an AP or hotspot.
"""

import os
import sys

from public import AP_IP, IP_ST, IP_ED
ap_password = None
ap_face = None
ap_ssid = None
out_face = None

def start_hostapd():
    """
    start hostapd to create an AP.
    """
    with open('/etc/hostapd.conf', 'w+') as f:
        if ap_password is not None:
            f.write('interface=' + ap_face + '\n' +
                    'ssid=' + ap_ssid + '\n' +
                    'channel=1' + '\n' +
                    'wpa=2' + '\n' +
                    'wpa_key_mgmt=WPA-PSK' + '\n' +
                    'wpa_pairwise=TKIP' + '\n' +
                    'rsn_pairwise=CCMP' + '\n' +
                    'wpa_passphrase=' + ap_password + '\n')
        else:
            f.write('interface=' + ap_face + '\n' +
                    'ssid=' + ap_ssid + '\n' +
                    'channel=1' + '\n')
    os.system('hostapd /etc/hostapd.conf')


def start_ip_forward():
    """
    start ip forward to create a hotspot.
    """
    os.system('echo \'1\' > /proc/sys/net/ipv4/ip_forward')
    os.system('iptables --flush')
    os.system('iptables -t nat --flush')
    os.system('iptables --delete-chain')
    os.system('iptables -t nat --delete-chain')
    os.system('iptables -t nat --append POSTROUTING --out-interface %s -j MASQUERADE' % out_face)
    os.system('iptables --append FORWARD --in-interface ' + ap_face + ' -j ACCEPT')


def start_dnsmasq(hostspot=False):
    """
    start dnsmasq to serve as DHCP server.
    """
    with open('/etc/dnsmasq.conf', 'w+') as f:
        f.write('interface=' + ap_face + '\n' +
                'dhcp-range=' + IP_ST + ',' + IP_ED + ',12h\n')
    os.system('dnsmasq')


def assign_ap_mac():
    """
    configure the AP interface with a random mac address
    """
    os.system('ifconfig ' + ap_face + ' down')
    os.system('macchanger ' + ap_face + ' -r')
    os.system('ifconfig ' + ap_face + ' up')


def assign_ap_ip():
    """
    configure the AP interface with a IP address
    """
    os.system('ifconfig ' + ap_face + ' ' + AP_IP + '/24 up')

def create(args):
    """
    create an AP, using the user specified interface.
    """
    global ap_face, ap_ssid, ap_password
    ap_face = args.interface
    ap_ssid = args.ssid
    ap_password = args.password

    print('Giving %s a random Mac address...' % ap_face)
    assign_ap_mac()

    print("\nConfiguring %s to ip %s..." % (ap_face, AP_IP))
    assign_ap_ip()

    print("\nStarting dnsmasq...")
    start_dnsmasq()

    print('\nStarting hostapd...')
    start_hostapd()


def hotspot(args):
    """
    create a hotspot, using the user specified interface, sharing another interface's network connection.
    """
    global ap_face, ap_ssid, ap_password, out_face
    ap_face = args.interface
    ap_ssid = args.ssid
    ap_password = args.password
    out_face = args.share_interface

    print("\nConfiguring %s to ip %s..." % (ap_face, AP_IP))
    assign_ap_ip()

    print("\nStarting dnsmasq...")
    start_dnsmasq(hostspot=True)

    print("\nStarting ip forward...")
    start_ip_forward()

    print('\nStarting hostapd...')
    start_hostapd()


def clear(args):
    """
    clear AP or hotspot
    """
    os.system("killall hostapd")
    os.system("killall dnsmasq")

    os.system('echo \'0\' > /proc/sys/net/ipv4/ip_forward')
    os.system('iptables --flush')
    os.system('iptables -t nat --flush')
    os.system('iptables --delete-chain')
    os.system('iptables -t nat --delete-chain')


def parse_args():
    """
    """
    import argparse
    parser = argparse.ArgumentParser(description="A script to create wifi AP.")
    subparsers = parser.add_subparsers()

    parser_1 = subparsers.add_parser('create', help='')
    parser_1.add_argument('-i', required=True, dest='interface', help='')
    parser_1.add_argument('-s', required=True, dest='ssid', help='')
    parser_1.add_argument('-p', dest='password', help='')
    parser_1.set_defaults(func=create)

    parser_2 = subparsers.add_parser('hotspot', help='')
    parser_2.add_argument('-i', required=True, dest='interface', help='')
    parser_2.add_argument('-s', required=True, dest='ssid', help='')
    parser_2.add_argument('-p', dest='password', help='')
    parser_2.add_argument('-si', dest='share_interface', required=True,  help='')
    parser_2.set_defaults(func=hotspot)

    parser_3 = subparsers.add_parser('clear', help='')
    parser_3.set_defaults(func=clear)

    args = parser.parse_args()
    if len(vars(args)) == 0:
        parser.print_help()
        sys.exit(-1)
    return args


if __name__ == '__main__':

    # check python version
    if sys.version[0] != '3':
        print("Python3 is needed.")
        sys.exit(-1)

    # check if has root privilege
    if os.geteuid() != 0:
        print("aphost must be run as root")
        sys.exit(-1)

    # parse args and execute
    args = parse_args()
    args.func(args)
