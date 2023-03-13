import random
from ipaddress import IPv4Network

from virtance.models import Virtance
from .models import Network, IPAddress


# First address is gateway, last address is broadcast
FIRST_IP_START = 2
LAST_IP_END = -1

def assign_free_ipv4_compute(virtance_id):
    virtance = Virtance.objects.get(id=virtance_id)
    virtances = Virtance.objects.filter(compute=virtance.compute, is_deleted=False)
    network = Network.objects.get(
        region=virtance.region,
        version=Network.IPv4, 
        type=Network.COMPUTE, 
        is_active=True, 
        is_deleted=False
    )
    assigned_ipv4_compute = IPAddress.objects.filter(network=network, virtance__in=virtances)
    ipv4net = IPv4Network(f"{network.cidr}/{network.netmask}")
    list_ipv4 = list(ipv4net)[FIRST_IP_START:LAST_IP_END]
    random.shuffle(list_ipv4)
    for ipaddr in list_ipv4:
        if str(ipaddr) not in [ip.address for ip in assigned_ipv4_compute]:
            IPAddress.objects.create(network=network, address=str(ipaddr), virtance=virtance)
            return True
    return False


def assign_free_ipv4_public(virtance_id):
    virtance = Virtance.objects.get(id=virtance_id)
    networks = Network.objects.filter(
        region=virtance.region, 
        version=Network.IPv4, 
        type=Network.PUBLIC, 
        is_active=True, 
        is_deleted=False
    )
    for net in networks:
        ipv4net = IPv4Network(f"{net.cidr}/{net.netmask}")
        list_ipv4 = list(ipv4net)[FIRST_IP_START:LAST_IP_END]
        random.shuffle(list_ipv4)
        for ipaddr in list_ipv4:
            if not IPAddress.objects.filter(network=net, address=str(ipaddr)).exists():
                IPAddress.objects.create(network=net, address=str(ipaddr), virtance=virtance)
                return True
    return False


def assign_free_ipv4_private(virtance_id):
    virtance = Virtance.objects.get(id=virtance_id)
    networks = Network.objects.filter(
        region=virtance.region,
        version=Network.IPv4, 
        type=Network.PRIVATE, 
        is_active=True, 
        is_deleted=False
    )
    for net in networks:
        ipv4net = IPv4Network(f"{net.cidr}/{net.netmask}")
        list_ipv4 = list(ipv4net)[FIRST_IP_START:LAST_IP_END]
        random.shuffle(list_ipv4)
        for ipaddr in list_ipv4:
            if not IPAddress.objects.filter(network=net, address=str(ipaddr)).exists():
                IPAddress.objects.create(network=net, address=str(ipaddr), virtance=virtance)
                return True
    return False


def assign_free_ipv6_public(virtance_id):
    pass
