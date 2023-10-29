import socket
import struct
import sys
import netifaces
from netifaces import AF_INET, AF_LINK
import binascii
import ipaddress

# Example:
# /data/ds_venv/bin/python3 arping.py  192.168.0.185 24:72:60:67:7c:c7 [count]
# According to iCatch, the WIFI module works in the way that it wakes and checks the packets with the AP every second in sleep mode.
# If the packet is not a broadcast (FF:FF:FF:FF:FF:FF), the AP will queue for the STA and deliver them to the STA while it wakes up.
# iCatch suggests that we use unicast arping and this can exploit the benefit of the AP so that the STA (camera) can reply to the arping.


def mac_to_binary(mac):
    return binascii.unhexlify(mac.replace(':', ''))


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print(f'Usage: {sys.argv[0]} camera_IP camera_mac [counts]')
        exit(0)

    str_dst_ip = sys.argv[1]
    str_dst_mac = sys.argv[2]
    count = int(sys.argv[3]) if len(sys.argv) > 3 else 5

    for str_if in netifaces.interfaces():
        network_info = netifaces.ifaddresses(str_if)
        str_src_ip, str_netmask = (network_info[AF_INET][0]['addr'], network_info[AF_INET][0]['netmask']) if AF_INET in network_info.keys() else (None, None)
        str_src_mac = network_info[AF_LINK][0]['addr'] if AF_LINK in network_info.keys() else None

        if not str_src_ip or not str_src_mac:
            continue

        if ipaddress.IPv4Address(str_dst_ip) in ipaddress.IPv4Network(f'{str_src_ip}/{ipaddress.IPv4Network((0, str_netmask)).prefixlen}', strict=False):
            # print(str_if, network_info)

            # eth_hdr = struct.pack("!6s6s2s", int(str_dst_mac.replace(':', ''), 16), int(str_src_mac.replace(':', ''), 16), '\x08\x06')
            eth_hdr = struct.pack("!6s6s2s", mac_to_binary(str_dst_mac), mac_to_binary(str_src_mac), b'\x08\x06')
            arp_hdr = struct.pack("!2s2s1s1s2s", b'\x00\x01', b'\x08\x00', b'\x06', b'\x04', b'\x00\x01')
            arp_sender = struct.pack("!6s4s", mac_to_binary(str_src_mac), socket.inet_aton(str_src_ip))
            arp_target = struct.pack("!6s4s", b'\x00\x00\x00\x00\x00\x00', socket.inet_aton(str_dst_ip))

            for i in range(count):
                try:
                    # send packet
                    with socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0806)) as rawSocketWrite:
                        rawSocketWrite.bind((str_if, socket.htons(0x0806)))
                        rawSocketWrite.send(eth_hdr + arp_hdr + arp_sender + arp_target)

                    with socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0806)) as rawSocketRead:
                        rawSocketRead.settimeout(0.5)
                        response = rawSocketRead.recvfrom(2048)
                        if str_dst_ip == socket.inet_ntoa(response[0][28:32]):
                            print(':'.join(binascii.hexlify(response[0][6:12]).swapcase().decode('ascii')[i:i + 2] for i in range(0, 12, 2)))
                            break
                except socket.timeout:
                    pass
            break
